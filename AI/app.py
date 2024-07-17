from datetime import time

from starlette.middleware.cors import CORSMiddleware

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



@app.get("/start")
def main():
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
