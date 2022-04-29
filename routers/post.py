from typing import List, Optional
from app import models, schemes, oauth2
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app.database import get_db

router = APIRouter(
    # allows removal of '/post' from the router tag
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemes.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemes.Post)
def create_posts(post: schemes.PostCreate, db: Session = Depends(get_db),
                 current_user: schemes.UserBase = Depends(oauth2.get_current_user)):
    print(current_user.id)
    # build the query
    new_post_query = models.Post(owner_id=current_user.id, **post.dict())
    # add the query to postgres
    db.add(new_post_query)
    # commit the staged query
    db.commit()
    # store the data added by postgres back to the original query variable
    db.refresh(new_post_query)
    return new_post_query


@router.get('/{id}', response_model=schemes.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemes.Post)
def update_post(id: int, post: schemes.PostCreate, db: Session = Depends(get_db),
                current_user= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    my_post = post_query.first()
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
    if my_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    post = post_query.first()
    return post
