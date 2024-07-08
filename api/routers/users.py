from ..db import supabase
from .. import schemas
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[schemas.User])
async def read_users():
    users = supabase.table("users").select("*").execute().data
    return users


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    try:
        user = supabase.table("users").insert(user.dict()).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return user.data[0]

@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int):
    user = supabase.table("users").delete().eq("id", user_id).execute().data
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]


@router.get("/{user_id}", response_model=List[schemas.PostOutList])
async def read_user_posts(user_id: int):
    posts = supabase.table("posts").select("*").eq("creator_id", user_id).execute().data
    for post in posts:
        post["creator"] = supabase.table("users").select("*").eq("id", post["creator_id"]).execute().data[0]
        post["comments"] = supabase.table("posts").select("*", count="exact").eq("reply_to", post["id"]).execute().count

    return posts


