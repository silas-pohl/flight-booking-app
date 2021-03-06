from uuid import UUID, uuid4
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import FLOAT, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class Airport(Base):
    __tablename__ = "airports"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    title = Column(String, index=True)


class Flight(Base):
    __tablename__ = "flights"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    departure_time_utc = Column(TIMESTAMP)
    arrival_time_utc = Column(TIMESTAMP)
    departure_airport_id = Column(
        UUID(as_uuid=True), ForeignKey("airports.id"))
    destination_airport_id = Column(
        UUID(as_uuid=True), ForeignKey("airports.id"))
    ticket_price_dollars = Column(FLOAT)
    seats = Column(Integer)

    departure_airport = relationship(
        "Airport", foreign_keys=[departure_airport_id])
    destination_airport = relationship(
        "Airport", foreign_keys=[destination_airport_id])


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    flight_id = Column(UUID(as_uuid=True), ForeignKey("flights.id"))
    created = Column(TIMESTAMP)

    owner = relationship("User", foreign_keys=[owner_id])
    flight = relationship("Flight", foreign_keys=[flight_id])


class VerificationRecord(Base):
    __tablename__ = "verification_records"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    email = Column(String)
    action = Column(String)
    verification_code = Column(Integer)
    created = Column(TIMESTAMP)

class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String, primary_key=True)