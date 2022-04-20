from typing import List
from app import models, schemes, utils
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import get_db

router = APIRouter(
    # allows removal of '/post' from the router tag
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemes.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemes.Post)
def create_posts(post: schemes.PostCreate, db: Session = Depends(get_db)):
    # build the query
    new_post_query = models.Post(**post.dict())
    # add the query to postgres
    db.add(new_post_query)
    # commit the staged query
    db.commit()
    # store the data added by postgres back to the original query variable
    db.refresh(new_post_query)
    return new_post_query


@router.get('/{id}', response_model=schemes.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemes.Post)
def update_post(id: int, post: schemes.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    my_post = post_query.first()
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    post = post_query.first()
    return post
