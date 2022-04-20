from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
from .database import engine, get_db
from . import models, schemes, utils
from routers import post, user
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

f = open('app/files/pw.txt', 'r')
pw = f.read()
f.close()

# allows path operations to be in different modules, by grabbing router object from post and user files
app.include_router(post.router)
app.include_router(user.router)


# Path (or Route) operation
@app.get("/")  # root path
# Path operation function
def root():
    # whatever is returned is what gets sent back to the user and Fast API converts it to JSON
    return {"message": "Welcome to my API !!!!! cool"}
