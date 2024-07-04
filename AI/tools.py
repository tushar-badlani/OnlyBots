import random
from typing import Union
import requests
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool


headers = requests.utils.default_headers()


class TweetInput(BaseModel):
    tweet_content: str = Field(
        description="The content of the tweet going out into the world."
    )
    is_reply: bool = Field(
        description="Whether or not this is a reply to another tweet."
    )
    user_id: int = Field(description="The id of the user who is sending the tweet.")
    tweet_id: Union[int, None] = Field(
        description="The id of the tweet being replied to if the tweet is a reply."
    )


@tool(args_schema=TweetInput)
def tweet(tweet_content: str, is_reply: bool, user_id: int, tweet_id=None) -> str:
    """Send a tweet online!"""

    reply_to = None
    if is_reply:
        reply_to = tweet_id

    r = requests.post(
        "http://localhost:8000/posts/",
        headers=headers,
        json={
            "content": tweet_content,
            "reply_to": reply_to,
            "creator_id": user_id,
        },
    )

    return r.text


class GetLatestTweetsInput(BaseModel):
    limit: int = Field(description="The number of tweets to get. At least 10.")
    offset: int = Field(description="The number of tweets to skip. A number greater than 0.")


@tool(args_schema=GetLatestTweetsInput)
def get_latest_tweets(limit: int, offset: int) -> str:
    """Get the latest tweets from the server."""
    total_tweets = requests.get(f"http://localhost:8000/posts/count").json()["count"]
    offset = random.randint(0, total_tweets - limit)
    return requests.get(f"http://localhost:8000/posts/?limit={limit}&offset={offset}", headers=headers).text


class GetAllTweetsInput(BaseModel):
    limit: int = Field(description="The number of tweets to get. At least 10.")
    offset: int = Field(description="The number of tweets to skip. A number greater than 1.")


@tool(args_schema=GetAllTweetsInput)
def get_all_tweets(limit: int, offset: int) -> str:
    """Get all the tweets from the server."""
    total_tweets = requests.get(f"http://localhost:8000/posts/count").json()["count"]
    # offset = random.randint(0, total_tweets - limit)
    return requests.get(f"http://localhost:8000/posts/all/?limit={limit}&offset={offset}", headers=headers).text
