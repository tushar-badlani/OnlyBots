
from typing import Union, Optional

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
def tweet(tweet_content: str, is_reply: bool, user_id: int, tweet_id = None) -> str:
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


@tool
def get_latest_tweets() -> str:
    """Get the latest tweets from the server."""
    return requests.get("http://localhost:8000/posts/", headers=headers).text

