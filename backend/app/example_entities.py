from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import crud, models, schemas


def create_airport(db: Session, title: str):
    db_airport = models.Airport(title=title)
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport


def create_example_entities(db: Session):
    if(crud.read_user_by_email(db=db, email="payments.flight.booking@gmail.com")):
        raise HTTPException(
            status_code=409, detail="Example user already exists, aborting example setup")

    example_user_1 = crud.create_user(
        db=db, email="payments.flight.booking@gmail.com", password="KRpgAbtlE8HL04coWc5B!", first_name="Flight", last_name="Booking")

    example_airport_1 = create_airport(db=db, title="JFK New York")
    example_airport_2 = create_airport(db=db, title="Munich Airport")

    example_flight_base_1 = schemas.FlightBase(
        departure_airport_id=example_airport_1.id,
        destination_airport_id=example_airport_2.id,
        departure_time_utc=datetime.now(),
        arrival_time_utc=datetime.now(),
        ticket_price_dollars=20.00,
        seats=24
    )

    example_flight_1 = crud.create_flight(db=db, flight=example_flight_base_1)

    example_ticket_1 = crud.create_user_ticket(
        db, user_id=example_user_1.id, ticket_flight_id=example_flight_1.id, created=datetime.now())

    return {"message": "Example entities set up"}
