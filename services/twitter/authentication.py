"""Twitter authenticator module."""
import logging
import os
from pydantic import BaseModel

import tweepy
from decouple import config
from utils.custom_exceptions.twitter_exceptions import (
    TwitterInvalidCredentialsException,
)

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

CONSUMER_KEY = config("CONSUMER_KEY")
CONSUMER_SECRET = config("CONSUMER_SECRET")
ACCESS_TOKEN = config("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")


class TwitterAuthenticatorData(BaseModel):
    """Basic Tweitter Atuth data model."""

    consumer_key: str = CONSUMER_KEY
    consumer_secret: str = CONSUMER_SECRET
    access_token: str = ACCESS_TOKEN
    access_token_secret: str = ACCESS_TOKEN_SECRET


class TwitterAuthenticator:

    """Twitter Authenticator class."""

    @staticmethod
    def authorizer() -> tweepy.OAuthHandler:
        """Twitter authorizer method.

        Returns
        -------
        `tweepy.OAuthHandler`
        """
        logger.info("Authenticating to Twitter")
        twitter_authenticator_data = TwitterAuthenticatorData()
        auth = tweepy.OAuthHandler(
            consumer_key=twitter_authenticator_data.consumer_key,
            consumer_secret=twitter_authenticator_data.consumer_secret,
        )
        auth.set_access_token(
            key=twitter_authenticator_data.access_token,
            secret=twitter_authenticator_data.access_token_secret,
        )

        return auth

    @classmethod
    def create_api(cls) -> tweepy.API:
        """Twitter API method.

        Returns
        -------
        `tweepy.API`
        """
        api = tweepy.API(
            auth_handler=cls.authorizer(), wait_on_rate_limit=True
        )
        if not api.verify_credentials():
            logger.error("Invalid credentials")
            raise TwitterInvalidCredentialsException(
                "Invalid credentials. Verify them"
            )
        logger.info("API client created successfully")
        return api
