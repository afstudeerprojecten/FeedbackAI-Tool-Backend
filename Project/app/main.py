from typing import Protocol
from fastapi import FastAPI, HTTPException, Depends, status
from enum import Enum
from sqlalchemy import Engine
from sqlalchemy.orm import Session
import os
from jose import jwt
from dataclasses import dataclass    
import app.models as models
from app.database import engine, SessionLocal


app = FastAPI()
models.Base.metadata.create_all(bind=engine)



@dataclass
class APIResponse:
    data: dict
    status: int = 200




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# No need for db_dependency annotation
def db_dependency():
    return Depends(get_db)


@app.get("/")
async def root():
    return {"message": "Welcome to the API, made with FastAPI!!"}
