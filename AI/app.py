from datetime import time

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from AI.main import get_character, get_emotion, get_prompt, agent_executor
from fastapi import FastAPI
from AI.tools import tweets
from AI.news import getNews


origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func= get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/start")
@limiter.limit("1/minute")
async def main(request: Request):
    tweets.clear()
    character, character_id = get_character()
    emotion = get_emotion()
    prompt = get_prompt(character, emotion, character_id)
    print(f"Character: {character}, Emotion: {emotion}")
    print(f"Prompt: {prompt}")

    agent_executor.invoke(
        {
            "input": prompt + " " + "Your user id is " + str(character_id),
        }
    )

    return tweets


@app.get("/news")
def news(category: str):
    return getNews(category)


@app.get("/")
def read_root():
    return {"Hello": "World"}
