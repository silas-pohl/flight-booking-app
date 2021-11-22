from typing import Collection
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import FLOAT, INTEGER, TIMESTAMP

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    tickets = relationship("Ticket", back_populates="owner")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    country = Column(String, index=True)

    airports = relationship("Airport", back_populates="city")


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    city_id = Column(Integer, ForeignKey("cities.id")) 
    
    city = relationship("City", back_populates="airports") 
    departing_flights = relationship("Flight", back_populates="airport")
    arriving_flights = relationship("Flight", back_populates="airport") 


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    departure_time_utc = Column(TIMESTAMP, index=True)
    arrival_time_utc = Column(TIMESTAMP, index=True)
    departure_airport_id = Column(Integer, ForeignKey("airports.id"))
    destination_airport_id = Column(Integer, ForeignKey("airports.id"))
    ticket_price_dollars = Column(FLOAT, index=True)
    max_tickets = Column(Integer, index=True)

    departure_airport = relationship("Airport", back_populates="flights")
    destination_airport = relationship("Airport", back_populates="flights")
    tickets = relationship("Ticket", back_populates="flights")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))

    owner = relationship("User", back_populates="tickets")
    flight = relationship("Flight", back_populates="tickets")


