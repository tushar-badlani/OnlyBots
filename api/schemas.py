from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    profile_pic: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime


class UserOut(User):
    bio: Optional[str] = None


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


class PostOutList(Post):
    comments: int


class PostOut(Post):
    comments: Optional[list[PostOutList]] = []


