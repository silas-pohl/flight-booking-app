from typing import Optional
from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/database")
def database():
    conn = psycopg2.connect(
        database = os.getenv('POSTGRES_DATABASE'),
        user = os.getenv('POSTGRES_USER'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'), 
        port = os.getenv('POSTGRES_PORT')
    )
    return {"data": "Opened database successfully"}