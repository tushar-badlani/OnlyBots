from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..utils import parse_results_posts

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[schemas.UserOut])
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
    p1 = aliased(models.Post)
    p2 = aliased(models.Post)
    u1 = aliased(models.User)

    reply_count = (
        db.query(func.count(p2.id))
        .where(p2.reply_to == p1.id)
        .correlate(p1)
        .label("reply_count")
    )

    query = db.query(
        p1.content.label("content"),
        p1.creator_id.label("creator_id"),
        p1.id.label("id"),
        p1.created_at.label("created_at"),
        u1.name.label("user_name"),
        u1.profile_pic.label("user_profile_pic"),
        u1.id.label("user_id"),
        u1.created_at.label("user_created_at"),
        reply_count
    ).join(u1, p1.creator_id == u1.id
    ).filter(p1.creator_id == user_id
    ).order_by(p1.created_at.desc())

    results = query.all()
    result_dict = parse_results_posts(results)
    return result_dict



@router.get("/user/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


