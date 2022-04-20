from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemes, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemes.UserOut)
def create_user(user: schemes.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.hash(user.password)
    add_user_query = models.User(**user.dict())
    db.add(add_user_query)
    db.commit()
    db.refresh(add_user_query)
    return add_user_query


@router.get('/{id}', response_model=schemes.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} was not found')
    return user


