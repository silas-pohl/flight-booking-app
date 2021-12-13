import re
from random import SystemRandom, sample
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
    allow_origins=[
        "http://localhost:5000",
        "https://frontend-flight-booking-app.herokuapp.com"
    ],
    allow_headers=[
        "Content-Type",
        "Authorization"
    ],
    allow_credentials=True,
    allow_methods=["*"],
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
        r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    if not (re.fullmatch(regex, data.email)) or (data.action not in ['register', 'login', 'reset']):
        print(
            f"LOG: Error: Invalid request with action {data.action} and email {data.email}")
        raise HTTPException(status_code=422, detail="Invalid request data")

    # Check if email already exists for register or not exists for login and reset
    if data.action == 'register' and crud.get_user_by_email(db, data.email):
        print(f"LOG: Error: Email {data.email} already exists")
        raise HTTPException(status_code=409, detail="Email already registered")
    elif data.action in ['login', 'reset'] and crud.get_user_by_email(db, data.email) is None:
        print(f"LOG: Error: Email {data.email} not registered")
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
    print(f"LOG: Info: Email with verificationcode sent to {data.email}")
    return data


@app.post('/register', response_model=schemas.RegisterData)
def register(data: schemas.RegisterData, db: Session = Depends(get_db)):
    '''Register user if verification code is valid'''

    # Validate request data
    mail_regex = re.compile(
        r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    pw_regex = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{12,}')
    if (
        len(data.first_name) < 2 or
        len(data.last_name) < 2 or
        not (re.fullmatch(mail_regex, data.email)) or
        not (re.fullmatch(pw_regex, data.password)) or
        len(str(data.verification_code)) != 8
    ):
        print(f"LOG: Error: Invalid username {data.email} or password")
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
    print(f"LOG: Info: Created user {data.email}")
    crud.delete_verification_record(db, data.email, 'register')
    return data


@app.post("/login", response_model=schemas.Token)
async def login(form_data: schemas.TokenLogin, response: Response, db: Session = Depends(get_db)):
    user = auth.authenticate_user(form_data.email, form_data.password, db)
    if not user:
        print(f"LOG: Error: Invalid username {form_data.email} or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"LOG: Info: Successful login for user {form_data.email}")
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
                        value=refresh_token,
                        domain="frontend-flight-booking.herokuapp.com",
                        httponly=True,
                        samesite="none",
                        secure=True)

    return {"access_token": access_token,
            "token_type": "bearer",
            "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES*60*1000}


@app.get("/refreshtoken", response_model=schemas.Token)
async def refreshtoken(response: Response, refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    email, admin = validate_token(refresh_token, db)
    if not email:
        print("LOG: Error: Invalid refreshtoken request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    crud.delete_refresh_token(db, refresh_token=refresh_token)

    access_token = auth.create_access_token(
        data={"sub": email, "admin": admin},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = auth.create_refresh_token(
        data={"sub": email, "admin": admin},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES+1),
        db=db
    )

    print("LOG: Info: Successful token refresh")
    response.set_cookie(key="refresh_token",
                        value=new_refresh_token,
                        domain="frontend-flight-booking.herokuapp.com",
                        httponly=True,
                        samesite="none",
                        secure=True)

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
    print("LOG: Info: Successful logout")
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
    print(f"LOG: Info: Tickets requested for user {current_user.email}")
    return crud.get_user_tickets(db, current_user.id)


@app.get("/me/tickets/{ticket_id}")
async def read_own_ticket(ticket_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    print(
        f"LOG: Info: Ticket {ticket_id} requested for user {current_user.email}")
    return crud.get_user_ticket(db, current_user.id, ticket_id)


@app.get("/airports")
async def get_all_airports(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    print(f"LOG: Info: Airports requested for user {current_user.email}")
    return crud.get_airports(db=db)


@app.get("/airports/{airport_id}", response_model=schemas.Airport)
async def get_all_airports(airport_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    print(
        f"LOG: Info: Airport {airport_id} requested for user {current_user.email}")
    return crud.get_airport(db=db, airport_id=airport_id)


@app.get("/flights")
async def get_all_flights(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    print(f"LOG: Info: All flights requested for user {current_user.email}")
    return crud.get_all_flights(db)


@app.get("/flights/{flight_id}", response_model=schemas.Flight)
async def get_flight(flight_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    print(
        f"LOG: Info: Flight {flight_id} requested for user {current_user.email}")
    return crud.get_flight(db, flight_id)


@app.post("/me/booking", response_model=schemas.TicketID)
async def book_flight(data: schemas.FlightID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    if current_user.is_admin:
        print(
            f"LOG: Error: Flight booking requested by admin user {current_user.email}")
        raise HTTPException(
            status_code=401, detail="Action not allowed for admins"
        )
    flight = crud.get_flight(db=db, flight_id=data.flight_id)
    booked_tickets = crud.get_booked_tickets_number(
        db=db, flight_id=data.flight_id)
    if (flight.seats - booked_tickets > 0):
        ticket = crud.create_user_ticket(
            db=db, user_id=current_user.id, flight_id=data.flight_id, created=datetime.now())
        print(
            f"LOG: Info: Flight {data.flight_id} booked for user {current_user.email}")
        return schemas.TicketID(ticket_id=ticket.id)
    raise HTTPException(
        status_code=409, detail="No more tickets available for this flight.")


@app.post("/me/cancellation")
async def cancel_flight(data: schemas.TicketID, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    if current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Action not allowed for admins"
        )
    user_ticket = crud.get_user_ticket(
        db=db, user_id=current_user.id, ticket_id=data.ticket_id)
    flight = crud.get_flight(db=db, flight_id=user_ticket.flight_id)
    if(((flight.departure_time_utc - datetime.now()).total_seconds() / 3600) > 48):
        print(
            f"LOG: Info: Flight {user_ticket.flight_id} cancelled for user {current_user.email}")
        return crud.delete_user_ticket(
            db=db, user_id=current_user.id, ticket_id=data.ticket_id)
    else:
        print(
            f"LOG: Error: Flight {user_ticket.flight_id} cannot be cancelled for user {current_user.email}: Less than 48h until takeoff")
        raise HTTPException(
            status_code=409, detail="Cancellation is only available until 48h before takeoff")


# Experimental

@app.post("/exampleentities")
async def create_example_entities(db: Session = Depends(get_db)):
    return example_entities.create_example_entities(db=db)

# Admin Routes


@app.get("/users")
async def get_all_users(current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    print(f"LOG: Info: All user info requested for admin {current_user.email}")
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
    print(
        f"LOG: Info: Flight from airport {flight.departure_airport_id} to airport {flight.destination_airport_id} at {flight.departure_time_utc} created by admin {current_user.email}")
    return crud.create_flight(db, flight)


@app.delete("/flights/{flight_id}", response_model=schemas.FlightID)
async def delete_flight(flight_id: uuid.UUID, current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session = Depends(get_db)):
    print(f"LOG: Info: Flight {flight_id} deleted by {current_user.email}")
    return crud.delete_flight(db=db, flight_id=flight_id)
