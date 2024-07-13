from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=List[schemas.PostOutList])
async def read_posts(limit: int = 5, offset: int = 0, db=Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).filter(models.Post.reply_to == None).limit(limit).offset(offset).all()
    for post in posts:
        post.comments = db.query(models.Post).filter(models.Post.reply_to == post.id).count()
        post.creator = db.query(models.User).filter(models.User.id == post.creator_id).first()
    return posts


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



@router.get("/all")
async def all_posts(limit: int =5, offset: int =0, db=Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).limit(limit).offset(offset).all()
    for post in posts:
        post.comments = db.query(models.Post).filter(models.Post.reply_to == post.id).count()
        post.creator = db.query(models.User).filter(models.User.id == post.creator_id).first()
    return posts



@router.get("/{post_id}", response_model=schemas.PostOut)
async def read_post(post_id: int, db=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.comments = db.query(models.Post).filter(models.Post.reply_to == post_id).count()
    post.creator = db.query(models.User).filter(models.User.id == post.creator_id).first()
    post.comments = db.query(models.Post).filter(models.Post.reply_to == post_id).all()
    for comment in post.comments:
        comment.comments = db.query(models.Post).filter(models.Post.reply_to == comment.id).count()
        comment.creator = db.query(models.User).filter(models.User.id == comment.creator_id).first()
    return post



# @router.delete("/{post_id}", response_model=schemas.Post)
# async def delete_post(post_id: int):
#     post = supabase.table("posts").delete().eq("id", post_id).execute().data
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     post = post[0]
#     post["creator"] = supabase.table("users").select("*").eq("id", post["creator_id"]).execute().data[0]
#     return post
