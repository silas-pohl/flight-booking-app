from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import FLOAT, TIMESTAMP

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    departure_time_utc = Column(TIMESTAMP, index=True)
    arrival_time_utc = Column(TIMESTAMP, index=True)
    departure_airport_id = Column(Integer, ForeignKey("airports.id"))
    destination_airport_id = Column(Integer, ForeignKey("airports.id"))
    ticket_price_dollars = Column(FLOAT, index=True)
    max_tickets = Column(Integer, index=True)

    departure_airport = relationship(
        "Airport", foreign_keys=[departure_airport_id])
    destination_airport = relationship(
        "Airport", foreign_keys=[destination_airport_id])


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))

    owner = relationship("User", foreign_keys=[owner_id])
    flight = relationship("Flight", foreign_keys=[flight_id])


class VerificationEntry(Base):
    __tablename__ = "verification_entries"

    email = Column(String, primary_key=True, index=True)
    verfication_code = Column(Integer, index=True)
    created = Column(TIMESTAMP, index=True)
