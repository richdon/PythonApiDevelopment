from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint


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


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


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


########## Vote ##########################
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
