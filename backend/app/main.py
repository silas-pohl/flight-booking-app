from typing import Optional, List
import psycopg2
import os
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register endpoint (works)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# Login endpoint

@app.post("/token", response_model=schemas.Token)
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

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return current_user


@app.get("/users/me/tickets/")
async def read_own_tickets(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session=Depends(get_db)):
    return crud.get_user_tickets(db, current_user.id) 


@app.get("/flights/{flight_id}", response_model=schemas.Flight)
async def get_flight(flight_id: int, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session=Depends(get_db)):
    return crud.get_flight(db, flight_id)


@app.post("/booking/{flight_id}", response_model=schemas.Ticket)
async def book_flight(flight_id: int, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session=Depends(get_db)):
    pass


@app.post("/cancellation/{ticket_id}")
async def cancel_flight(ticket_id: int, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session=Depends(get_db)):
    pass


# Admin Routes

@app.post("/flights", response_model=schemas.Flight)
async def create_flight(flight: schemas.FlightBase, current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session=Depends(get_db)):
    return crud.create_flight(db, flight)


@app.put("/flights/{flight_id}", response_model=schemas.Flight)
async def alter_flight(flight_id: int, flight: schemas.FlightBase, current_user: schemas.User = Depends(auth.get_current_active_admin_user), db: Session=Depends(get_db)):
    pass
