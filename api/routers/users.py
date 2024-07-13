from sqlalchemy.orm import Session

from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[schemas.User])
async def read_users(search: str = None, db: Session = Depends(get_db)):
    if search:
        users = db.query(models.User).filter(models.User.name.ilike(f"%{search}%")).all()
    else:
        users = db.query(models.User).all()
    return users



@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, profile_pic=user.profile_pic)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @router.delete("/{user_id}", response_model=schemas.User)
# async def delete_user(user_id: int):
#     # user = supabase.table("users").delete().eq("id", user_id).execute().data
#     # if not user:
#     #     raise HTTPException(status_code=404, detail="User not found")
#     # return user[0]


@router.get("/{user_id}", response_model=List[schemas.PostOutList])
async def read_user_posts(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    posts = db.query(models.Post).filter(models.Post.creator_id == user_id).order_by(models.Post.created_at.desc()).all()
    for post in posts:
        post.comments = db.query(models.Post).filter(models.Post.reply_to == post.id).count()
        post.creator = user
    return posts



