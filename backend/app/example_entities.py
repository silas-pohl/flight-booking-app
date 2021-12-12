from datetime import datetime, timedelta
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
    if(crud.get_user_by_email(db=db, email="payments.flight.booking@gmail.com")):
        raise HTTPException(
            status_code=409, detail="Example user already exists, aborting example setup")

    crud.create_admin_user(db=db, email="payments.flight.booking@gmail.com", password="TestT3stT€st", first_name="Flight", last_name="Booking")

    airport_1 = create_airport(db=db, title="JFK - New York Airport")
    airport_2 = create_airport(db=db, title="MUC - Munich Airport")
    airport_3 = create_airport(db=db, title="FRA - Frankfurt Airport")
    airport_4 = create_airport(db=db, title="LHR - Heathrow Airport")
    airport_5 = create_airport(db=db, title="LCY - London City Airport")
    airport_6 = create_airport(db=db, title="BRU - Brussels Airport")

    flight_base_1 = schemas.FlightBase(
        departure_airport_id=airport_1.id,
        destination_airport_id=airport_2.id,
        departure_time_utc=datetime.now() + timedelta(hours=96),
        arrival_time_utc=datetime.now() + timedelta(hours=100),
        ticket_price_dollars=120.00,
        seats=40
    )
    flight_base_2 = schemas.FlightBase(
        departure_airport_id=airport_4.id,
        destination_airport_id=airport_1.id,
        departure_time_utc=datetime.now() + timedelta(hours=200),
        arrival_time_utc=datetime.now() + timedelta(hours=205),
        ticket_price_dollars=100.00,
        seats=35
    )
    flight_base_3 = schemas.FlightBase(
        departure_airport_id=airport_5.id,
        destination_airport_id=airport_6.id,
        departure_time_utc=datetime.now() + timedelta(hours=16),
        arrival_time_utc=datetime.now() + timedelta(hours=19),
        ticket_price_dollars=70.00,
        seats=10
    )
    flight_base_4 = schemas.FlightBase(
        departure_airport_id=airport_6.id,
        destination_airport_id=airport_1.id,
        departure_time_utc=datetime.now() + timedelta(hours=75),
        arrival_time_utc=datetime.now() + timedelta(hours=83),
        ticket_price_dollars=180.00,
        seats=5
    )
    flight_base_5 = schemas.FlightBase(
        departure_airport_id=airport_3.id,
        destination_airport_id=airport_6.id,
        departure_time_utc=datetime.now() + timedelta(hours=210),
        arrival_time_utc=datetime.now() + timedelta(hours=212),
        ticket_price_dollars=80.00,
        seats=85
    )

    crud.create_flight(db=db, flight=flight_base_1)
    crud.create_flight(db=db, flight=flight_base_2)
    crud.create_flight(db=db, flight=flight_base_3)
    crud.create_flight(db=db, flight=flight_base_4)
    crud.create_flight(db=db, flight=flight_base_5)

    return {"message": "Example entities set up"}
