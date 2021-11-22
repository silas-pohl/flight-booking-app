from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime, timezone

# JWT
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Items: Basic Class for Flights, Cities and Airports 
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

# Owned Items: Basic Class for Tickets
class OwnedItemBase(ItemBase):
    owner_id: int


# Cities
class CityBase(ItemBase):
    country: str


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
        
# Airports
class AirportBase(ItemBase):
    city_id: int


class Airport(AirportBase):
    id: int

    class Config:
        orm_mode = True


# Flights
class FlightBase(ItemBase):
    departure_airport_id: int
    destination_airport_id: int
    departure_time_utc: datetime
    arrival_time_utc: datetime
    ticket_price_dollars: float
    max_tickets: int


class Flight(FlightBase):
    id: int

    class Config:
        orm_mode = True


# Tickets
class TicketBase(OwnedItemBase):
    id: int 


class Ticket(TicketBase):
    flight_id: str

    class Config:
        orm_mode = True


# Users 
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    items: List[ItemBase] = []

    class Config:
        orm_mode = True


class UserLogin(User):
    hashed_password: str


class UserCreate(UserBase):
    password: str