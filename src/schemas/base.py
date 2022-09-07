"""Base schemas."""

from pydantic import BaseModel

from models.enums import SentimentClassificationEnum


class TweetBase(BaseModel):
    """Tweet response model."""

    id: int
    tweet_text: str
    user_screen_name: str


class ResponseBase(BaseModel):
    """Base response model."""

    detail: str


class HashtagBase(BaseModel):
    """Base Hashtag model."""

    query: str


class CountTweetBase(BaseModel):
    """Base Count model."""

    sentiment_classificator: SentimentClassificationEnum
    count: int


class MetricsBase(BaseModel):
    """Base metrics model"""

    tweets_count: int
    most_used_hashtag: str
    hashtag_count: dict
    most_retweeted: str
    # most_liked: str
    # most_clicked: str
    # average_retweets: float
    # average_likes: float
    # percentiles: Dict
