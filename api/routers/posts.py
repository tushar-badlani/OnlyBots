from ..db import supabase
from .. import schemas
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.get("/", response_model=List[schemas.PostOutList])
async def read_posts(limit: int=5, offset: int=0):
    posts = supabase.table("posts").select("*").is_("reply_to", "null").order("created_at", desc=False).range(offset, offset+limit).execute().data
    for post in posts:
        post["creator"] = supabase.table("users").select("*").eq("id", post["creator_id"]).execute().data[0]
        post["comments"] = supabase.table("posts").select("*", count= "exact").eq("reply_to", post["id"]).execute().count

    # posts.sort(key=lambda x: x["comments"], reverse=True)
    return posts


@router.post("/", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate):
    try:
        post = supabase.table("posts").insert(post.dict()).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    post = post.data[0]
    post["creator"] = supabase.table("users").select("*").eq("id", post["creator_id"]).execute().data[0]
    return post


@router.get("/{post_id}", response_model=schemas.PostOut)
async def read_post(post_id: int):
    post = supabase.table("posts").select("*").eq("id", post_id).execute().data
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = post[0]
    post["creator"] = supabase.table("users").select("*").eq("id", post["creator_id"]).execute().data[0]
    post["comments"] = supabase.table("posts").select("*").eq("reply_to", post_id).execute().data
    for comment in post["comments"]:
        comment["creator"] = supabase.table("users").select("*").eq("id", comment["creator_id"]).execute().data[0]
    return post


@router.delete("/{post_id}", response_model=schemas.Post)
async def delete_post(post_id: int):
    post = supabase.table("posts").delete().eq("id", post_id).execute().data
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = post[0]
    post["creator"] = supabase.table("users").select("*").eq("id", post["creator_id"]).execute().data[0]
    return post




