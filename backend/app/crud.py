from sqlalchemy.orm import Session

from . import models, schemas, auth


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    psw_hash = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=psw_hash, first_name=user.first_name, last_name=user.last_name, is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id)


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_airport(db: Session, airport_id: int):
    return db.query(models.Airport).filter(models.Airport.id == airport_id)


def get_airports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Airport).offset(skip).limit(limit).all()


def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id)


def get_suitable_flights(db: Session, departure_airport_id: int, destination_airport_id: int):
    return db.query(models.Flight).filter(models.Flight.departure_airport_id == departure_airport_id,
    models.Flight.destination_airport_id == destination_airport_id)


def get_all_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()


def get_user_tickets(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).filter(models.Ticket.owner_id==user_id).offset(skip).limit(limit).all()


def create_user_ticket(db: Session, ticket: schemas.Ticket, user_id: int, ticket_flight_id: int):
    db_ticket = models.Ticket(**ticket.dict(), owner_id=user_id, flight_id=ticket_flight_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
