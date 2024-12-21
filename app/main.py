from fastapi import FastAPI, HTTPException, Response, status, Depends, utils
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import psycopg2, time
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, users, auth, vote
from app import schemas
from . import models, utils
from .database import engine, sessionLocal, get_db
origins=["*"]
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="openpg",
            password="openpgpwd",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print(f"Database connection failed: {error}")
        time.sleep(2)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)