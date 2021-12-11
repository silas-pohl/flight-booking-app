import re
from random import SystemRandom
from datetime import timedelta, datetime
from sqlalchemy.sql.sqltypes import DateTime
from fastapi import Depends, FastAPI, HTTPException, status, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth, mail
import uuid
from .database import SessionLocal, engine
from . import example_entities

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5000',
                   'https://frontend-flight-booking-app.herokuapp.com/'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/verificationcode', response_model=schemas.EmailVerification)
def verificationcode(data: schemas.EmailVerification, db: Session = Depends(get_db)):
    '''Send verification code to email adress to authorize respective action.'''

    # Validate request data
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    if not (re.fullmatch(regex, data.email)) or (data.action not in ['register', 'login', 'reset']):
        raise HTTPException(status_code=422, detail="Invalid request data")

    # Check if email already exists for register or not exists for login and reset
    if data.action == 'register' and crud.get_user_by_email(db, data.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    elif data.action in ['login', 'reset'] and crud.get_user_by_email(db, data.email) is None:
        raise HTTPException(status_code=404, detail="Email not registered")

    # Delete all records older than 5mins from verification_records table
    crud.delete_expired_verification_records(db, timedelta(minutes=5))

    # Check if verification_code in verification_codes table or needs to be generated and stored
    verification_record = crud.read_verification_record(
        db, data.email, data.action)
    if (verification_record):
        verification_code = verification_record.verification_code
    else:
        verification_code = SystemRandom().randint(10000000, 99999999)
        crud.create_verification_record(
            db, data.email, data.action, verification_code, datetime.now())

    # Send mail with verification token and mirror request data
    mail.send_verification_code(data.email, verification_code)
    return data


@app.post('/register', response_model=schemas.RegisterData)
def register(data: schemas.RegisterData, db: Session = Depends(get_db)):
    '''Register user if verification code is valid'''

    # Validate request data
    mail_regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
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
    verification_record = crud.read_verification_record(
        db, data.email, 'register')
    if not (verification_record) or int(data.verification_code) != verification_record.verification_code:
        raise HTTPException(
            status_code=403, detail="Incorrect verification code")

    # Create user, delete verification record and mirror request data
    crud.create_user(db, data.email, data.password,
                     data.first_name, data.last_name)
    crud.delete_verification_record(db, data.email, 'register')
    return data


@app.post("/login", response_model=schemas.Token)
async def login(form_data: schemas.TokenLogin, response: Response, db: Session = Depends(get_db)):
    user = auth.authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={"sub": user.email, "admin": user.is_admin},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user.email, "admin": user.is_admin},
        expires_delta=timedelta(days=auth.ACCESS_TOKEN_EXPIRE_MINUTES+1),
        db=db
    )

    response.set_cookie(key="refresh_token",
                        value=refresh_token, httponly=True)

    return {"access_token": access_token,
            "token_type": "bearer",
            "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES*60*1000}


@app.get("/refreshtoken", response_model=schemas.Token)
async def refreshtoken(response: Response, refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    email, admin = validate_token(refresh_token, db)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={"sub": email, "admin": admin},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = auth.create_refresh_token(
        data={"sub": email, "admin": admin},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES+1),
        db=db
    )

    response.set_cookie(key="refresh_token",
                        value=new_refresh_token, httponly=True)

    crud.delete_refresh_token(db, refresh_token=refresh_token)

    return {"access_token": access_token,
            "token_type": "bearer",
            "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES*60*1000}


def validate_token(token: str, db: Session):
    db_token = crud.get_refresh_token(db, refresh_token=token)
    if not db_token:
        return False, False

    userinfo = auth.verify_token(token)
    if not userinfo[0]:
        return False, False
    return userinfo


@app.delete("/logout")
async def delete_refresh_token(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    crud.delete_refresh_token(db, refresh_token=refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Routes


@app.get("/me", response_model=schemas.UserBase)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return {
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }


@app.get("/me/tickets")
async def read_own_tickets(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_user_tickets(db, current_user.id)


@app.get("/me/tickets/{ticket_id}")
async def read_own_ticket(ticket_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_user_ticket(db, current_user.id, ticket_id)


@app.get("/airports")
async def get_all_airports(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_airports(db=db)


@app.get("/airports/{airport_id}", response_model=schemas.Airport)
async def get_all_airports(airport_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_airport(db=db, airport_id=airport_id)


@app.get("/flights")
async def get_all_flights(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_all_flights(db)


@app.get("/flights/{flight_id}", response_model=schemas.Flight)
async def get_flight(flight_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_flight(db, flight_id)


@app.post("/me/booking", response_model=schemas.TicketID)
async def book_flight(data: schemas.FlightID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    flight = crud.get_flight(db=db, flight_id=data.flight_id)
    booked_tickets = crud.get_booked_tickets_number(
        db=db, flight_id=data.flight_id)
    if (flight.seats - booked_tickets > 0):
        ticket = crud.create_user_ticket(
            db=db, user_id=current_user.id, flight_id=data.flight_id, created=datetime.now())
        return schemas.TicketID(ticket_id=ticket.id)
    raise HTTPException(
        status_code=409, detail="No more tickets available for this flight.")


@app.post("/me/cancellation")
async def cancel_flight(data: schemas.TicketID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    user_ticket = crud.get_user_ticket(
        db=db, user_id=current_user.id, ticket_id=data.ticket_id)
    if(datetime.now() - user_ticket.created < timedelta(hours=48)):
        return crud.delete_user_ticket(
            db=db, user_id=current_user.id, ticket_id=data.ticket_id)
    else:
        raise HTTPException(
            status_code=409, detail="Cancellation is only available until 48h before takeoff")


# Experimental

@app.post("/exampleentities")
async def create_example_entities(db: Session = Depends(get_db)):
    return example_entities.create_example_entities(db=db)

# Admin Routes


@app.get("/users")
async def get_all_users(current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/flights", response_model=schemas.Flight)
async def create_flight(flight: schemas.FlightBase, current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    if flight.arrival_time_utc < flight.departure_time_utc:
        raise HTTPException(
            status_code=422, detail="Arrival time must not be earlier than departure time.")
    if flight.seats < 0:
        raise HTTPException(
            status_code=422, detail="Number of available seats must be greater than or equal to zero.")
    if flight.ticket_price_dollars < 0.0:
        raise HTTPException(
            status_code=422, detail="Ticket price must be greater than or equal to zero.")

    return crud.create_flight(db, flight)


@app.delete("/flights/{flight_id}", response_model=schemas.FlightID)
async def delete_flight(flight_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    return crud.delete_flight(db=db, flight_id=flight_id)
