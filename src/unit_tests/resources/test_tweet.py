"""Unit tests for resources/twitter.py module."""
import unittest
import os, sys
from unittest.mock import MagicMock, call, patch
from controllers.tweets.tweets_db import DBTweetController
from resources.tweet import (
    get_twitter_metrics
)
from fixtures import mock_tweet_query, mock_hashtags_count

lib_to_patch = "resources.tweet"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 


class TestTweet(unittest.TestCase):

    """
    Test tweet resource.
    """

    def setUp(self) -> None:
        return super().setUp()


    @patch(f"{lib_to_patch}.DBTweetController", autospec=True)
    @patch(f"{lib_to_patch}.count_hashtags", autospec=True, return_value=mock_hashtags_count)
    # @patch(f"{lib_to_patch}.ReturnMetrics", autospec=True)
    def test_get_twitter_metrics_ok(self):
        db_tweet_controller = DBTweetController()
        db_tweet_controller.fetch_twitter_metrics.return_value = mock_tweet_query
        response = get_twitter_metrics()
        db_tweet_controller.fetch_twitter_metrics.assert_called_once()
        self.AssertEquals(response, """{
                'detail': 'Metrics obtained successfully',
                'tweets_count': 4,
                'most_used_hashtag': 'sarasa',
                'hashtag_count': {
                    'verso': 1,
                    'sarasa': 4,
                    'chamuyo': 1
                },
                'most_retweeted': ''
            }""")


    @patch(f"{lib_to_patch}.DBTweetController", autospec=True)
    @patch(f"{lib_to_patch}.count_hashtags", autospec=True, return_value=0)
    def test_get_twitter_metrics_no_results(self):
        db_tweet_controller = DBTweetController()
        db_tweet_controller.fetch_twitter_metrics.return_value = []
        response = get_twitter_metrics()
        db_tweet_controller.fetch_twitter_metrics.assert_called_once()
        self.AssertEquals(response, """{
                'detail': 'Metrics obtained successfully',
                'tweets_count': 0,
                'most_used_hashtag': '',
                'hashtag_count': {},
                'most_retweeted': ''
            }""")

