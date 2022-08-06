"""Unit tests for services/twitter_data.py module."""
import unittest
from unittest.mock import MagicMock, call, patch

from services.twitter.twitter_data import (
    TweetRelevantData,
    TwitterDataCollector,
)
from utils.custom_exceptions.twitter_exceptions import (
    MissingDataTweetException,
)
from utils.tweet import tweet_utils


lib_to_patch = "services.twitter.twitter_data"


class MockTweetUser(object):
    """Mock tweet User."""

    def __init__(self, screen_name) -> None:
        """Init method."""
        self.screen_name = screen_name


class MockTweetStatus(object):
    """Mock Tweet Status object"""

    def __init__(self, **kwargs) -> None:
        """Init method."""
        self.created_at = kwargs.get("created_at", "")
        self.id = kwargs.get("id", "")
        self.id_str = kwargs.get("id_str", "")
        self.full_text = kwargs.get("full_text", "")
        self.user = kwargs.get("user", "")
        self.entities = kwargs.get("entities", "")


tweets_response = [
    MockTweetStatus(
        **{
            "created_at": "Wed Oct 10 20:19:24 +0000 2018",
            "id": 1050118621198921728,
            "id_str": "1050118621198921728",
            "full_text": "Tweet text example",
            "user": MockTweetUser(**{"screen_name": "@testuser"}),
            "entities": {},
        }
    ),
    MockTweetStatus(
        **{
            "created_at": "Wed Oct 10 20:19:24 +0000 2018",
            "id": 1050118621198921728,
            "id_str": "1050118621198921728",
            "full_text": "Tweet text example 1",
            "user": MockTweetUser(**{"screen_name": "@testuser1"}),
            "entities": {},
        }
    ),
]

formatted_tweets = [
    {
        "created_at": "Wed Oct 10 20:19:24 +0000 2018",
        "id_str": "1050118621198921728",
        "tweet_text": "Tweet text example",
        "user_screen_name": "@testuser",
    },
    {
        "created_at": "Wed Oct 10 20:19:24 +0000 2018",
        "id_str": "1050118621198921728",
        "tweet_text": "Tweet text example 1",
        "user_screen_name": "@testuser1",
    },
]

tweet_with_line_breaks = MockTweetStatus(
    **{
        "created_at": "Wed Oct 10 20:19:24 +0000 2018",
        "id": 1050118621198921728,
        "id_str": "1050118621198921728",
        "full_text": "Tweet\ntext\nexample",
        "user": MockTweetUser(**{"screen_name": "@testuser"}),
        "entities": {},
    }
)

tweet_text_with_no_line_breaks = "Tweet text example"


class TestTwitterData(unittest.TestCase):

    """Test Twitter Data."""

    def setUp(self) -> None:
        """SetUp."""
        self.query = "#query_test"
        self.extra_kwargs = {
            "lang": "test_lang",
            "count": "test_count",
            "tweet_mode": "test_tweet_mode",
        }

    @patch(f"{lib_to_patch}.TwitterAuthenticator.create_api", autospec=True)
    @patch(
        f"{lib_to_patch}.TwitterDataCollector.extract_relevant_tweet_data",
        autospec=True,
    )
    def test_get_data_by_single_query(
        self, mock_extract_relevant_data, mock_create_api
    ):
        """test Get data using a query."""
        twitter_data_collector = TwitterDataCollector()
        twitter_data_collector.api = MagicMock(
            autospec=twitter_data_collector.api
        )
        twitter_data_collector.api.search.return_value = tweets_response
        twitter_data_collector.get_data_by_single_query(
            query=self.query,
            **self.extra_kwargs,
        )
        mock_create_api.assert_called_once()

        self.assertEqual(
            [call(tweet=tweet_response) for tweet_response in tweets_response],
            mock_extract_relevant_data.call_args_list,
        )
        self.assertEqual(2, len(mock_extract_relevant_data.call_args_list))

    def test_extract_relevant_tweet_data(self):
        """Test method to extract relevant data from tweets."""
        for i, tweet in enumerate(tweets_response):
            result = TwitterDataCollector.extract_relevant_tweet_data(
                tweet=tweet
            )
            self.assertDictEqual(result, formatted_tweets[i])

    def test_missing_attribute_data(self):
        """Test an exception raises when there is missing attributes."""
        tweet = tweets_response[0]
        del tweet.full_text
        with self.assertRaises(MissingDataTweetException) as ctx:
            TwitterDataCollector.extract_relevant_tweet_data(tweet=tweet)
        self.assertEqual("Tweet has a missing attribute.", str(ctx.exception))

    def test_format_search_tweets_keywords(self):
        """Test function to get the formatted keywords."""
        expected_res = {
            "lang": "en",
            "count": 10,
            "tweet_mode": "extended",
        }
        res = tweet_utils.format_search_tweets_keywords()

        self.assertDictEqual(expected_res, res)


class TestTweetRelevantDataModel(unittest.TestCase):

    """Test the TweetRelevantData model."""

    def setUp(self) -> None:
        """SetUp."""

    def test_transform_tweet_text(self):
        """Test tweet text is transformed correctly (line breaks removed)."""
        tweet_result = TweetRelevantData(
            tweet_text=tweet_with_line_breaks.full_text,
            id_str=tweet_with_line_breaks.id_str,
            user_screen_name=tweet_with_line_breaks.user.screen_name,
            created_at=tweet_with_line_breaks.created_at,
        )
        self.assertEqual(
            tweet_result.tweet_text, tweet_text_with_no_line_breaks
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
