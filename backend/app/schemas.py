from typing import List, Optional

from pydantic import BaseModel

# JWT
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

# Items: placeholders for flights 
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class ItemCreate(ItemBase):
    pass

# Users 
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class UserLogin(User):
    hashed_password: str


class UserCreate(UserBase):
    password: str
