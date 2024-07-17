import os
import random
from typing import Union
import requests
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from AI.news import getNews
import dotenv

dotenv.load_dotenv()

URL = os.getenv("URL")

headers = requests.utils.default_headers()

tweets = []

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
        f"{URL}posts/",
        headers=headers,
        json={
            "content": tweet_content,
            "reply_to": reply_to,
            "creator_id": user_id,
        },
    )

    if r.status_code == 201:
        post = r.json()
        tweets.append(post["id"])
        return post
    else:
        return r.text


class GetTrendingTweetsInput(BaseModel):
    limit: int = Field(description="The number of tweets to get. At least 20.")
    offset: int = Field(description="The number of tweets to skip. A number greater than 0.")


@tool(args_schema=GetTrendingTweetsInput)
def get_trending_tweets(limit: int, offset: int) -> str:
    """Get the trending tweets from the server."""
    return requests.get(f"{URL}posts/trending/?limit={limit}&offset={offset}", headers=headers).text


class GetAllTweetsInput(BaseModel):
    limit: int = Field(description="The number of tweets to get. At least 10.")
    offset: int = Field(description="The number of tweets to skip. A number greater than 1.")


@tool(args_schema=GetAllTweetsInput)
def get_all_tweets(limit: int, offset: int) -> str:
    """Get all the tweets from the server."""
    return requests.get(f"{URL}posts/all/?limit={limit}&offset={offset}", headers=headers).text


class GetLatestNewsInput(BaseModel):
    category: str = Field(description="""The category of news to get. The valid categories are categories = ["national", "business", "sports", "world", "politics", "technology", "startup", "entertainment", "miscellaneous", "hatke", "science", "automobile"]""")


@tool(args_schema=GetLatestNewsInput)
def get_latest_news(category: str) -> str:
    """Get latest news to tweet about"""
    categories = ["all", "national","business", "sports", "world", "politics", "technology", "startup", "entertainment", "miscellaneous", "hatke", "science", "automobile"]
    if category not in categories:
        return {"error" : "Please select valid category"}
    return getNews(category)