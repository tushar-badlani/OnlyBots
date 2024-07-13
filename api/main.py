from fastapi import FastAPI
from . import db, models
from .db import engine
from .routers import users, posts
from fastapi.middleware.cors import CORSMiddleware


origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "welcome to my api!!"}


app.include_router(users.router)
app.include_router(posts.router)
