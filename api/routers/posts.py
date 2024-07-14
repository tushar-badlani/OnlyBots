from sqlalchemy import func
from sqlalchemy.orm import aliased

from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models import Post, User
from ..utils import parse_results_post, parse_results_posts

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=List[schemas.PostOutList])
async def read_posts(limit: int = 5, offset: int = 0, db=Depends(get_db)):
    p1 = aliased(Post)
    p2 = aliased(Post)
    u1 = aliased(User)

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
    ).order_by(p1.created_at.desc()
    ).filter(p1.reply_to == None).limit(limit
    ).offset(offset)

    results = query.all()
    result_dict = parse_results_posts(results)
    return result_dict





@router.post("/")
async def create_post(post: schemas.PostCreate, db=Depends(get_db)):
    try:
        new_post = models.Post(content=post.content, creator_id=post.creator_id, reply_to=post.reply_to)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/count")
async def count_posts(db=Depends(get_db)):
    count = db.query(models.Post).filter(models.Post.reply_to == None).count()
    return {"count": count}


@router.get("/trending", response_model=List[schemas.PostOutList])
async def trending_posts(limit: int = 5, offset: int = 0, db=Depends(get_db)):
    p1 = aliased(Post)
    p2 = aliased(Post)
    u1 = aliased(User)

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
    ).order_by(reply_count.desc()
    ).limit(limit
    ).offset(offset)

    results = query.all()
    result_dict = parse_results_posts(results)
    return result_dict

@router.get("/{post_id}", response_model=schemas.PostOut)
async def read_post(post_id: int, db=Depends(get_db)):
    p1 = aliased(Post)
    p2 = aliased(Post)
    p3 = aliased(Post)  # New alias for counting replies
    u1 = aliased(User)
    u2 = aliased(User)

    # Subquery to count replies for each comment
    reply_count = (
        db.query(func.count(p3.id))
        .where(p3.reply_to == p2.id)
        .correlate(p2)
        .label("reply_count")
    )

    query = db.query(
        p1.content.label("post_content"),
        p1.creator_id.label("post_creator_id"),
        p1.reply_to.label("post_reply_to"),
        p1.id.label("post_id"),
        p1.created_at.label("post_created_at"),
        u1.name.label("user_name"),
        u1.profile_pic.label("user_profile_pic"),
        u1.id.label("user_id"),
        u1.created_at.label("user_created_at"),
        p2.content.label("comment_content"),
        p2.creator_id.label("comment_creator_id"),
        p2.reply_to.label("comment_reply_to"),
        p2.id.label("comment_id"),
        p2.created_at.label("comment_created_at"),
        u2.name.label("comment_creator_name"),
        u2.profile_pic.label("comment_creator_profile_pic"),
        u2.id.label("comment_creator_id"),
        u2.created_at.label("comment_creator_created_at"),
        reply_count  # Add the subquery to count replies
    ).join(u1, p1.creator_id == u1.id
    ).outerjoin(p2, p1.id == p2.reply_to
    ).outerjoin(u2, p2.creator_id == u2.id
    ).filter(p1.id == post_id)

    results = query.all()
    result_dict = parse_results_post(results)

    return result_dict
# @router.delete("/{post_id}", response_model=schemas.Post)
# async def delete_post(post_id: int):
#     post = supabase.table("posts").delete().eq("id", post_id).execute().data
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     post = post[0]
#     post["creator"] = supabase.table("users").select("*").eq("id", post["creator_id"]).execute().data[0]
#     return post
