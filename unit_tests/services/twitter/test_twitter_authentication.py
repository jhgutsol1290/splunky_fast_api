"""Test Twitter authentication module."""
import os
import unittest
from unittest.mock import MagicMock, patch

from utils.custom_exceptions.twitter_exceptions import (
    TwitterInvalidCredentialsException,
)

lib_to_patch = "services.twitter.authentication"


with patch.dict(
    os.environ,
    {
        "CONSUMER_KEY": "Testing_Consumer_Key",
        "CONSUMER_SECRET": "Testing_Consumer_Secret",
        "ACCESS_TOKEN": "Testing_Access_Token",
        "ACCESS_TOKEN_SECRET": "Testing_Access_Token_Secret",
    },
    clear=True,
):
    from services.twitter.authentication import TwitterAuthenticator


class TestTwitterAuthenticator(unittest.TestCase):

    """Test Twitter authenticator class."""

    def setUp(self) -> None:
        """SetUp."""

    @patch(f"{lib_to_patch}.tweepy.OAuthHandler")
    def test_twitter_auth(self, mock_oauth_handler):
        """Twitter auth module test."""
        mock_oauth_handler.return_value.set_access_token = MagicMock()
        TwitterAuthenticator.authorizer()

        mock_oauth_handler.assert_called_once_with(
            consumer_key="Testing_Consumer_Key",
            consumer_secret="Testing_Consumer_Secret",
        )
        mock_oauth_handler.return_value.set_access_token.assert_called_once_with(
            key="Testing_Access_Token", secret="Testing_Access_Token_Secret"
        )

    @patch(f"{lib_to_patch}.TwitterAuthenticator.authorizer")
    @patch(f"{lib_to_patch}.tweepy.API")
    def test_create_unsuccessful_api(self, mock_API, mock_twitter_auth):
        """Twitter create api test."""
        mock_API.return_value.verify_credentials.return_value = False
        with self.assertRaises(TwitterInvalidCredentialsException) as ctx:
            TwitterAuthenticator.create_api()

        self.assertTrue("Invalid credentials.", str(ctx.exception))
        mock_twitter_auth.assert_called_once()
        mock_API.assert_called_once()

    @patch(f"{lib_to_patch}.TwitterAuthenticator.authorizer")
    @patch(f"{lib_to_patch}.tweepy.API")
    def test_create_successful_api(self, mock_API, mock_twitter_auth):
        """Twitter create api test."""
        mock_API.return_value.verify_credentials.return_value = True
        TwitterAuthenticator.create_api()

        mock_twitter_auth.assert_called_once()
        mock_API.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
