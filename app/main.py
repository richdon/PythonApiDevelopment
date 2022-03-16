from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
from .database import engine, get_db
from . import models, schemas
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

f = open('files/pw.txt', 'r')
pw = f.read()
f.close()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fast-api-social-media-app', user='postgres',
                                password=pw, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfully created')
        break

    except Exception as e:
        if isinstance(e, OperationalError):
            if 'password authentication failed' in e.args[0]:
                print("Error: Wrong password entered for database. Exiting...")
                exit(code=1)
        print("Connection to database failed. Retrying connection in 2 seconds...")
        print(f"Error: {e}")
        time.sleep(2)


# Path (or Route) operation
@app.get("/")  # root path
# Path operation function
def root():
    # whatever is returned is what gets sent back to the user and Fast A
    # PI converts it to JSON
    return {"message": "Welcome to my API !!!!! cool"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # build the query
    new_post_query = models.Post(**post.dict())
    # add the query to postgres
    db.add(new_post_query)
    # commit the staged query
    db.commit()
    # store the data added by postgres back to the original query variable
    db.refresh(new_post_query)
    return new_post_query


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    #
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'post with id {id} does not exist')
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # if not updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'post with id {id} was not found')
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    my_post = post_query.first()
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    post = post_query.first()
    return post


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    add_user_query = models.User(**user.dict())
    db.add(add_user_query)
    db.commit()
    db.refresh(add_user_query)
    return add_user_query
