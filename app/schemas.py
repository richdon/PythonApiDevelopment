from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


########## User ############################
class UserBase(BaseModel):
    email: EmailStr

    # Needed for Fast api to read orm models
    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    password: str


########## Post ##########################
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    # Needed for Fast api to read orm models
    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


########## Login ###########################
class UserLogin(BaseModel):
    email: EmailStr
    password: str


######## access token ####################
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
