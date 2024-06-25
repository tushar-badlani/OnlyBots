from fastapi import FastAPI
from . import db
from .routers import users, posts

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to my api!!"}


app.include_router(users.router)
app.include_router(posts.router)