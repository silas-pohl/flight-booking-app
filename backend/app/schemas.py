from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime, timezone

# JWT
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

# Items: placeholders for flights 
class ItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class Item(ItemBase):
    owner_id: int

    class Config:
        orm_mode = True

class ItemCreate(ItemBase):
    pass

# Cities
class City(ItemBase):
    country: str

    class Config:
        orm_mode = True
        
# Airports
class Airport(ItemBase):
    city_id: int

    class Config:
        orm_mode = True

# Flights
class Flight(ItemBase):
    departure_airport_id: int
    destination_airport_id: int
    departure_time_utc: datetime
    arrival_time_utc: datetime
    ticket_price_dollars: float
    max_tickets: int

    class Config:
        orm_mode = True

# Tickets
class Ticket(Item):
    flight_id: str

# Users 
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class UserLogin(User):
    hashed_password: str


class UserCreate(UserBase):
    password: str