"""Extract Twitter data."""
from typing import Dict, List

import tweepy
from services.abstract.abstract_data_collector import DataCollector
from services.twitter.authentication import TwitterAuthenticator
from utils.custom_exceptions.twitter_exceptions import (
    MissingDataTweetException,
)
from utils.tweet.tweet_utils import line_breaks_to_spaces
from pydantic import BaseModel, validator


class TweetRelevantData(BaseModel):
    """Tweets relevant data base model."""

    tweet_text: str
    id_str: str
    user_screen_name: str
    created_at: str

    @validator("tweet_text")
    def transform_tweet_text(cls, text):
        """Transforms tweet text to not include NBSP."""
        return line_breaks_to_spaces(text=text)


class TwitterDataCollector(DataCollector):

    """Twitter data collector class."""

    def __init__(self, retweets: bool = False) -> None:
        """Init method.

        Autorizes to the twitter api.

        Returns
        -------
        `None`
        """
        self.api = TwitterAuthenticator.create_api()
        self.retweets = retweets
        self.tweets_list = []

    def get_data_by_single_query(
        self, *, query: str, **kwargs: Dict
    ) -> List[Dict]:
        """
        Searching Twitter data given a query string.

        Using search_tweets method gets max. 100 tweets.

        Parameters
        ----------
        query: `str`
            query string to search for.

        kwargs: `Dict`
            Extra keyword arguments passed to the function.

        Returns
        -------
        `List[Dict]`
        """
        query = query if self.retweets else f"{query} -filter:retweets"
        self.tweets_list = [
            self.extract_relevant_tweet_data(tweet=tweet)
            for tweet in self.api.search(q=query, **kwargs)
        ]
        print(f"Count tweets extracted: {len(self.tweets_list)}")
        print(self.tweets_list)
        return self.tweets_list

    @staticmethod
    def extract_relevant_tweet_data(
        tweet: tweepy.models.Status,
    ) -> Dict:
        """Get relevant data from the tweet object.

        Parameters
        ----------
        tweet: `Dict`
            Complete tweet object.

            See https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

        Returns
        -------
        `Dict`
            Relevant Tweet data.

        Raises
        ------
        MissingDataTweetException
        """
        try:
            return TweetRelevantData(
                **{
                    "tweet_text": tweet.full_text,
                    "id_str": tweet.id_str,
                    "user_screen_name": tweet.user.screen_name,
                    "created_at": str(tweet.created_at),
                }
            ).dict()
        except AttributeError as e:
            raise MissingDataTweetException(
                "Tweet has a missing attribute."
            ) from e
