from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime


class PostBase(BaseModel):
    content: str
    creator_id: int
    reply_to: Optional[int] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    creator: User


class PostOut(Post):
    comments: Optional[list[Post]] = []


class PostOutList(Post):
    comments: int
