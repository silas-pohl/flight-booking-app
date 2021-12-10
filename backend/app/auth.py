from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, crud, models
from .database import SessionLocal, engine

import os

models.Base.metadata.create_all(bind=engine)

# Secret key
# Generate using: openssl rand -hex 32
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
REFRESH_TOKEN_SECRET = os.getenv('REFRESH_TOKEN_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Helper functions
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta], db: Session):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)
    if not crud.get_refresh_token(db, encoded_jwt):
      crud.add_refresh_token(db, encoded_jwt)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET,
                             algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        is_admin: bool = payload.get("admin")
        if email is None:
            return None, False
        return email, is_admin
    except JWTError:
        return None, False


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET,
                             algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_admin_user(
        current_user: schemas.User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return current_user
