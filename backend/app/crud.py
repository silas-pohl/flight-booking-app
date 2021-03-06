from datetime import datetime, timedelta
import uuid
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from . import models, schemas, auth

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Object not found"
)

# ----------------------------------------------------------------------------------------------------------------------
# USERS


def get_user(db: Session, user_id: uuid.UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, email: str, password: str, first_name: str, last_name: str):
    psw_hash = auth.get_password_hash(password)
    db_user = models.User(email=email, hashed_password=psw_hash, first_name=first_name,
                          last_name=last_name, is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_admin_user(db: Session, email: str, password: str, first_name: str, last_name: str):
    psw_hash = auth.get_password_hash(password)
    db_user = models.User(email=email, hashed_password=psw_hash, first_name=first_name,
                          last_name=last_name, is_admin=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ----------------------------------------------------------------------------------------------------------------------
# Refresh tokens


def add_refresh_token(db: Session, refresh_token: str):
    db_token = models.RefreshTokens(token=refresh_token)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_refresh_token(db: Session, refresh_token: str):
    return db.query(models.RefreshTokens).filter(models.RefreshTokens.token == refresh_token).first()


def delete_refresh_token(db: Session, refresh_token: str):
    db.query(models.RefreshTokens).filter(
        models.RefreshTokens.token == refresh_token).delete()
    db.commit()
    return


# ----------------------------------------------------------------------------------------------------------------------


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

    get_airport(db, flight.departure_airport_id)
    get_airport(db, flight.destination_airport_id)

    db_flight = models.Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def delete_flight(db: Session, flight_id: uuid.UUID):

    get_flight(db, flight_id=flight_id)

    db.query(models.Ticket).filter(
        models.Ticket.flight_id == flight_id).delete()
    db.query(models.Flight).filter(models.Flight.id == flight_id).delete()
    db.commit()
    return schemas.FlightID(flight_id=flight_id)


def get_booked_tickets_number(db: Session, flight_id: uuid.UUID):
    return db.query(models.Ticket).filter(models.Ticket.flight_id == flight_id).count()


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


def create_user_ticket(db: Session, user_id: uuid.UUID, flight_id: uuid.UUID, created: datetime):
    db_ticket = models.Ticket(
        owner_id=user_id, flight_id=flight_id, created=created)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def delete_user_ticket(db: Session, user_id: uuid.UUID, ticket_id: uuid.UUID):
    db.query(models.Ticket).filter(models.Ticket.id == ticket_id,
                                   models.Ticket.owner_id == user_id).delete()
    db.commit()
    print(ticket_id)
    return {ticket_id}

# ----------------------------------------------------------------------------------------------------------------------
# VERIFICATION RECORDS


def create_verification_record(db: Session, email: str, action: str, verification_code: int, created: datetime):
    db_verification_record = models.VerificationRecord(
        email=email, action=action, verification_code=verification_code, created=created
    )
    db.add(db_verification_record)
    db.commit()
    db.refresh(db_verification_record)


def read_verification_record(db: Session, email: str, action: str):
    try:
        db_verification_record = db.query(models.VerificationRecord)\
            .filter(models.VerificationRecord.email == email, models.VerificationRecord.action == action).one()
        return db_verification_record
    except sqlalchemy.exc.NoResultFound:
        return None


def delete_verification_record(db: Session, email: str, action: str):
    db.query(models.VerificationRecord)\
        .filter(models.VerificationRecord.email == email, models.VerificationRecord.action == action).delete()
    db.commit()


def delete_expired_verification_records(db: Session, maximum_age: timedelta):
    db.query(models.VerificationRecord)\
        .filter(datetime.now() - models.VerificationRecord.created > maximum_age).delete()
    db.commit()
# ----------------------------------------------------------------------------------------------------------------------
