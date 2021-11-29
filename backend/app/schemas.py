from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel

import uuid

# JWT


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# AirportBase: Basic Class for Airports
class AirportBase(BaseModel):
    title: str
    description: Optional[str] = None


# Airports
class Airport(AirportBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# Flights
class FlightBase(BaseModel):
    departure_airport_id: uuid.UUID
    destination_airport_id: uuid.UUID
    departure_time_utc: datetime
    arrival_time_utc: datetime
    ticket_price_dollars: float
    seats: int


class Flight(FlightBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# Owned Items: Basic Class for Tickets
class OwnedItemBase(BaseModel):
    owner_id: uuid.UUID


# Tickets
class TicketBase(OwnedItemBase):
    flight_id: uuid.UUID


class Ticket(TicketBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# Users
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class User(UserBase):
    id: uuid.UUID
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UserLogin(User):
    hashed_password: str


class UserCreate(UserBase):
    password: str


# Email verification entry
class EmailVerificationEntry(BaseModel):
    email: str
    verification_code: int
    created: datetime

    class Config:
        orm_mode = True
