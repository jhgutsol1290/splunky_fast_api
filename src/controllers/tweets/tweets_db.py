"""Tweet controller."""
from typing import Dict, List


from sqlalchemy import select, func

from database.db import database
from models import hashtag, sentiment_classificator, tweet


from controllers.abstract.abstract_db_tweet import IDBTweetController
from models.enums import SentimentClassificationEnum
from schemas.base import CountTweetBase
from schemas.responses.tweet import ClassificatedTweetsHashtag, TweetOut


class DBTweetController(IDBTweetController):

    """Tweet controller class."""

    @staticmethod
    async def get_tweets_without_hashtag() -> List[TweetOut]:
        """Retrieve all tweets without hashtag."""
        query = tweet.select().where(tweet.c.hashtag_id == None)
        return await database.fetch_all(query=query)

    @staticmethod
    async def get_tweet_without_hashtag_by_id(tweet_id: int) -> TweetOut:
        """Retrieve single tweet without hashtag."""
        query = tweet.select().where(
            tweet.c.hashtag_id == None, tweet.c.id == tweet_id
        )
        return await database.fetch_one(query=query)

    @staticmethod
    async def get_classificated_tweets_by_hashtag(
        hashtag_query: str,
    ) -> List[ClassificatedTweetsHashtag]:
        """Retrieve single tweet without hashtag."""
        query = (
            select(
                tweet.c.id,
                tweet.c.tweet_text,
                tweet.c.user_screen_name,
                hashtag.c.title,
                sentiment_classificator.c.sentiment_score,
                sentiment_classificator.c.sentiment_classification,
            )
            .select_from(tweet.join(hashtag).join(sentiment_classificator))
            .where(hashtag.c.title == hashtag_query)
        )
        return await database.fetch_all(query=query)

    @staticmethod
    async def get_count_by_sentiment_classificator(
        sentiment_classificator_query: str,
    ) -> CountTweetBase:
        """Get count of records using the given sentiment classificator.

        Parameters
        ----------
        sentiment_classificator_query: `str`
            Input sentiment classificator.

        Returns
        -------
        `CountTweetBase`
        """
        query = select(func.count()).where(
            sentiment_classificator.c.sentiment_classification
            == sentiment_classificator_query
        )
        count_ = await database.execute(query=query)
        return {
            "sentiment_classificator": sentiment_classificator_query,
            "count": count_,
        }

    @classmethod
    async def get_total_count(cls) -> List[CountTweetBase]:
        """Get total count of records.

        Returns
        -------
        `List[CountTweetBase]`
        """
        total_count = [
            await cls.get_count_by_sentiment_classificator(
                sentiment_classificator_query=item.value
            )
            for item in SentimentClassificationEnum
        ]

        return total_count

    @staticmethod
    @database.transaction()
    async def insert_sentiment_classificted_tweet(
        hashtag_data: Dict,
        tweets_data: List[Dict],
        sentiments_data: List[Dict],
    ) -> None:
        """Insert hashtag, tweet and classificator.

        Parameters
        ----------
        hashtag_data: `Dict`
            Hashtag to be inserted into the DB.

        tweets_data: `List[Dict]`
            Tweet data to be inserted into the DB.

        sentiments_data: `List[Dict]`
            Sentiment data to be inserted into the DB.

        Returns
        -------
        `None`
        """
        hashtag_id = await database.execute(
            hashtag.insert().values(hashtag_data)
        )
        for tweet_data, sentiment_data in zip(tweets_data, sentiments_data):
            tweet_data["hashtag_id"] = hashtag_id
            tweet_id = await database.execute(
                tweet.insert().values(tweet_data)
            )
            sentiment_data["id"] = tweet_id
            await database.execute(
                sentiment_classificator.insert().values(sentiment_data)
            )

    @staticmethod
    async def fetch_twitter_metrics() -> list:
        """Retrieve all the tweets and their hashtags."""
        
        query = select(
            tweet.c.id,
            hashtag.c.title
        ).select_from(tweet.join(hashtag))

        return await database.fetch_all(query=query)
