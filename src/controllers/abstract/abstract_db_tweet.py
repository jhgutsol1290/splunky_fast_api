from abc import ABC, abstractmethod
from typing import Dict, List
from schemas.base import CountTweetBase

from schemas.responses.tweet import (
    ClassificatedTweetsHashtag,
    TweetOut,
)


class IDBTweetController(ABC):

    """Interface TweetController."""

    @staticmethod
    @abstractmethod
    async def get_tweets_without_hashtag() -> List[TweetOut]:
        """Retrieve all tweets without hashtag from DB."""

    @staticmethod
    @abstractmethod
    async def get_tweet_without_hashtag_by_id() -> TweetOut:
        """Retrieve single tweet without hashtag from DB."""

    @staticmethod
    @abstractmethod
    async def get_classificated_tweets_by_hashtag() -> List[
        ClassificatedTweetsHashtag
    ]:
        """Retrieve single tweet without hashtag."""

    @staticmethod
    @abstractmethod
    async def get_count_by_sentiment_classificator() -> Dict:
        """Count of records with the given input."""

    @classmethod
    @abstractmethod
    async def get_total_count(cls) -> List[CountTweetBase]:
        """Get total count of records."""

    @staticmethod
    @abstractmethod
    async def insert_sentiment_classificted_tweet() -> None:
        """Inserts data to DB."""
