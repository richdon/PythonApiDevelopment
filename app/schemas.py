from datetime import datetime
from pydantic import BaseModel, EmailStr


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


class UserBase(BaseModel):
    email: EmailStr
    password: str

    # Needed for Fast api to read orm models
    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    pass
