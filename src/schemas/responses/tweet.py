"""Response schemas."""

from typing import List
from models.enums import SentimentClassificationEnum
from schemas.base import CountTweetBase, TweetBase, ResponseBase


class TweetOut(TweetBase):
    """Tweet Out response schema."""

    id_str: str
    created_at: str


class ClassificatedTweetsHashtag(TweetBase):
    """Classficated tweets our schema."""

    title: str
    sentiment_score: float
    sentiment_classification: SentimentClassificationEnum


class ResponseTweetNoHashtagOut(ResponseBase):
    """Response Tweet Out no hashtag schema."""

    data: TweetOut | None


class ResponseTweetsNoHashtagOut(ResponseBase):
    """Response Tweets Out no hashtag schema."""

    data: List[TweetOut | None]


class ResponseClassificatedTweetsHashtag(ResponseBase):
    """Response Classificated Tweets Hashtag schema."""

    data: List[ClassificatedTweetsHashtag | None]


class ResponseCountTweets(ResponseBase):
    """Response CountTweets."""

    # data: Union[List[CountTweetBase], CountTweetBase]
    data: List[CountTweetBase] | CountTweetBase
