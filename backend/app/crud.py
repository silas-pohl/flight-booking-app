from datetime import datetime
import uuid
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode

from fastapi import HTTPException, status

from . import models, schemas, auth

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Object not found"
)


def get_user(db: Session, user_id: uuid.UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    psw_hash = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=psw_hash, first_name=user.first_name,
                          last_name=user.last_name, is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_airport(db: Session, airport_id: uuid.UUID):
    try:
        return db.query(models.Airport).filter(models.Airport.id == airport_id).one()
    except sqlalchemy.exc.NoResultFound as nrf:
        raise not_found_exception from nrf


def get_airports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Airport).offset(skip).limit(limit).all()


def get_flight(db: Session, flight_id: uuid.UUID):
    try:
        return db.query(models.Flight).filter(models.Flight.id == flight_id).one()
    except sqlalchemy.exc.NoResultFound as nrf:
        raise not_found_exception from nrf


def get_all_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def create_flight(db: Session, flight: schemas.FlightBase):
    db_flight = models.Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def delete_flight(db: Session, flight_id: uuid.UUID):
    db.query(models.Flight).filter(models.Flight.id == flight_id).delete()
    db.commit()
    return flight_id


def get_user_ticket(db: Session, user_id: uuid.UUID, ticket_id: uuid.UUID):
    try:
        return db.query(models.Ticket)\
            .filter(models.Ticket.id == ticket_id, models.Ticket.owner_id == user_id).one()
    except sqlalchemy.exc.NoResultFound as nrf:
        raise not_found_exception from nrf


def get_user_tickets(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket)\
        .filter(models.Ticket.owner_id == user_id)\
        .offset(skip).limit(limit).all()


def create_user_ticket(db: Session, ticket: schemas.Ticket, user_id: uuid.UUID, ticket_flight_id: uuid.UUID):
    db_ticket = models.Ticket(
        **ticket.dict(), owner_id=user_id, flight_id=ticket_flight_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def create_verification_entry(db: Session, email: str, verification_code: int, created: datetime):
    db_verification_entry = models.VerificationEntry(
        email, verification_code, created)
    db.add(db_verification_entry)
    db.commit()
    db.refresh(db_verification_entry)


def get_verification_entry(db: Session, email: str):
    try:
        db_verification_entry = db.query(models.VerificationEntry)\
            .filter(models.VerificationEntry.email == email).one()
        return db_verification_entry
    except sqlalchemy.exc.NoResultFound as nrf:
        raise not_found_exception from nrf


def delete_verification_entry(db: Session, email: str):
    db.query(models.VerificationEntry).filter(
        models.VerificationEntry.email == email).delete()
    db.commit()
