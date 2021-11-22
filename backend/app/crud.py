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
    db_user = models.User(email=user.email, hashed_password=psw_hash, full_name=user.full_name, is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()


def get_user_tickets(db: Session, user_id: int,skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).filter(models.Ticket.owner_id==user_id).offset(skip).limit(limit).all()


def create_user_ticket(db: Session, ticket: schemas.Ticket, user_id: int, ticket_flight_id: int):
    db_ticket = models.Ticket(**ticket.dict(), owner_id=user_id, flight_id=ticket_flight_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
