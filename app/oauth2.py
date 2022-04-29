from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import schemes, database, models
from .config import settings

# SECRET_KEY
# Algorithm
# Expiration time

# pass the auth login path function endpoint name
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, creds_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if not id:
            raise creds_exception
        token_data = schemes.TokenData(id=id)
    except JWTError:
        raise creds_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Could not validate credentials',
                                    headers={'WWW-Authenticate': 'Bearer'})
    token = verify_access_token(token, creds_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
