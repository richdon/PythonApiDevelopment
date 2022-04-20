from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database, schemes, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemes.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    # create a token
    data = {'user_id': user.id}
    access_token = oauth2.create_access_token(data)
    # return token
    return {'access_token': access_token, 'token_type': 'bearer'}
