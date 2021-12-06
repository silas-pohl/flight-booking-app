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
class FlightID(BaseModel):
    flight_id: uuid.UUID


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
class TicketID(BaseModel):
    ticket_id: uuid.UUID


class TicketBase(OwnedItemBase):
    flight_id: uuid.UUID


class Ticket(TicketBase):
    id: uuid.UUID
    created: datetime

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


class EmailVerificationEntryBase(BaseModel):
    email: str


class EmailVerificationEntry(EmailVerificationEntryBase):
    verification_code: int
    created: datetime

    class Config:
        orm_mode = True


# -----------------------------------------------------------------------------
class TokenLogin(BaseModel):
    username: str
    password: str


class EmailVerification(BaseModel):
    email: str
    action: str


class RegisterData(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    verification_code: int


class LoginData(BaseModel):
    email: str
    password: str
    verification_code: int

# -----------------------------------------------------------------------------


class OrderID(BaseModel):
    order_id: str
