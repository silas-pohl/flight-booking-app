from typing import Optional, List
import psycopg2
import os
import re
from random import SystemRandom
from datetime import timedelta, datetime
from sqlalchemy.sql.sqltypes import DateTime
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth, mail, payments
import uuid
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5000', 'https://frontend-flight-booking-app.herokuapp.com/'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.post('/verificationcode', response_model=schemas.EmailVerification)
def verificationcode(data: schemas.EmailVerification, db: Session = Depends(get_db)):
    '''Send verification code to email adress to authorize respective action.'''

    # Validate request data
    regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    if not (re.fullmatch(regex, data.email)) or (data.action not in ['register', 'login', 'reset']): 
        raise HTTPException(status_code=422, detail="Invalid request data")

    # Check if email already exists for register or not exists for login and reset
    if data.action == 'register' and crud.read_user_by_email(db, data.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    elif data.action in ['login', 'reset'] and crud.read_user_by_email(db, data.email) is None:
        raise HTTPException(status_code=404, detail="Email not registered")

    # Delete all records older than 5mins from verification_records table
    crud.delete_expired_verification_records(db, timedelta(minutes=5))

    # Check if verification_code in verification_codes table or needs to be generated and stored
    verification_record = crud.read_verification_record(db, data.email, data.action)
    if (verification_record):
        verification_code = verification_record.verification_code
    else:
        verification_code = SystemRandom().randint(10000000, 99999999)
        crud.create_verification_record(db, data.email, data.action, verification_code, datetime.now())

    # Send mail with verification token and mirror request data
    mail.send_verification_code(data.email, verification_code)
    return data

@app.post('/register', response_model=schemas.RegisterData)
def register(data: schemas.RegisterData, db: Session = Depends(get_db)):
    '''Register user if verification code is valid'''

    # Validate request data
    mail_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    pw_regex = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{12,}')
    if (
        len(data.first_name) < 2 or
        len(data.last_name) < 2 or
        not (re.fullmatch(mail_regex, data.email)) or
        not (re.fullmatch(pw_regex, data.password)) or
        len(str(data.verification_code)) != 8
    ): 
        raise HTTPException(status_code=422, detail="Invalid request data")

    # Check if email and verificaion code not match
    verification_record = crud.read_verification_record(db, data.email, 'register')
    if not (verification_record) or data.verification_code != verification_record.verification_code:
        raise HTTPException(status_code=403, detail="Incorrect verification code")

    # Create user, delete verification record and mirror request data
    crud.create_user(db, data.email, data.password, data.first_name, data.last_name)
    crud.delete_verification_record(db, data.email, 'register')
    return data

"""
@app.post('/login', response_model=schemas.LoginData)
def login(data: schemas.LoginData, db: Session = Depends(get_db)):
    '''Login user if verification code is valid'''

    # Validate request data???

    # Check if email and verificaion code not match
    verification_record = crud.read_verification_record(db, data.email, 'login')
    if not (verification_record) or data.verification_code != verification_record.verification_code:
        raise HTTPException(status_code=403, detail="Incorrect verification code")

    user = crud.read_user_by_email(db, data.email)
    if not user or :
        raise HTTPException(status_code=403, detail="Incorrect email or password")
    return data
"""

# Register endpoint (works)

#@app.post("/users/", response_model=schemas.User)
#def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#    db_user = crud.get_user_by_email(db, email=user.email)
#    if db_user:
#        raise HTTPException(status_code=400, detail="Email already registered")
#    return crud.create_user(db=db, user=user)


# Login endpoint

#@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    user = authenticate_user(form_data.username, form_data.password, next(db))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "admin":user.is_admin}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user


# Routes


@app.get("/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return {
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }


@app.get("/me/tickets/")
async def read_own_tickets(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_user_tickets(db, current_user.id)


@app.get("/me/tickets/{ticket_id}")
async def read_own_ticket(ticket_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_user_ticket(db, current_user.id, ticket_id)


@app.get("/flights/")
async def get_all_flights(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_all_flights(db)


@app.get("/flights/{flight_id}", response_model=schemas.Flight)
async def get_flight(flight_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_flight(db, flight_id)


@app.post("/me/booking/", response_model=schemas.Ticket)
async def book_flight(flight_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    pass


@app.post("/me/cancellation/")
async def cancel_flight(ticket_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    pass


@app.post("/order")
async def create_order(fligth_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    departure_airport_id = uuid.uuid4()
    destination_airport_id = uuid.uuid4()
    departure_time_utc = datetime.now()
    arrival_time_utc = datetime.now()
    ticket_price_dollars = 1.2
    seats = 3
    id = uuid.uuid4
    flight = schemas.Flight(departure_airport_id, destination_airport_id,
                            departure_time_utc, arrival_time_utc, ticket_price_dollars, seats, id)
    return payments.create_order.create_order(flight=flight, user=current_user)

# Admin Routes


@app.get("/users")
async def get_all_users(current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/flights/", response_model=schemas.Flight)
async def create_flight(flight: schemas.FlightBase, current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    return crud.create_flight(db, flight)


@app.delete("/flights/{flight_id}", response_model=schemas.Flight)
async def alter_flight(flight_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    return crud.delete_flight(db, flight_id)
