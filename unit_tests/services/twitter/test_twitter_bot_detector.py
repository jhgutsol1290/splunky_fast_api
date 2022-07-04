"""Test twitter bot detector module."""
from typing import Dict
import unittest
from unittest.mock import MagicMock, patch

from services.twitter.twitter_bot_detector import TwitterAccountsBotDetector
from utils.custom_exceptions.twitter_exceptions import MaxBotAccountsPerRequets


lib_to_patch = "services.twitter.twitter_bot_detector"

MOCK_ACCOUNT = "@test_user"
MOCK_ACCOUNTS_LST = [
    (MOCK_ACCOUNT, 0.2, False),
    (MOCK_ACCOUNT + "_1", 0.7, True),
]


def helper_botometer_response(account: str, overall: float) -> Dict:
    """Helper mock function to generate botometer response.

    Parameters
    ----------
    account: `str`
        Mock twitter account name

    overall: `float`
        Mock overall result

    Returns
    -------
    `Dict`
    """
    return {
        "raw_scores": {
            "english": {
                "astroturf": 0.11,
                "fake_follower": 0.12,
                "financial": 0.0,
                "other": 0.36,
                "overall": overall,
                "self_declared": 0.25,
                "spammer": 0.0,
            },
            "universal": {
                "astroturf": 0.2,
                "fake_follower": 0.13,
                "financial": 0.01,
                "other": 0.41,
                "overall": 0.31,
                "self_declared": 0.31,
                "spammer": 0.02,
            },
        },
        "user": {
            "majority_lang": "en",
            "user_data": {
                "id_str": "44196397",
                "screen_name": account.split("@")[1],
            },
        },
    }


mock_botometer_accounts_response = [
    (
        mock_account,
        helper_botometer_response(account=mock_account, overall=overall),
    )
    for mock_account, overall, _ in MOCK_ACCOUNTS_LST
]

formatted_is_bot_accounts = [
    {
        "user_screen_name": mock_account,
        "botometer_score": overall,
        "is_bot": is_bot,
    }
    for mock_account, overall, is_bot in MOCK_ACCOUNTS_LST
]


class TestTwitterBotDetector(unittest.TestCase):

    """Test Twitter Bot Detector class."""

    def setUp(self) -> None:
        """SetUp."""

    @patch(
        f"{lib_to_patch}.botometer",
    )
    @patch(
        f"{lib_to_patch}.TwitterAccountsBotDetector.format_is_bot_account",
    )
    def test_check_accounts(
        self, mock_format_is_bot_account, mock_botometer
    ) -> None:
        """Test check_accounts method."""
        mock_botometer.Botometer = MagicMock()
        twitter_accounts_bot_detector = TwitterAccountsBotDetector(
            botometer_api=mock_botometer.Botometer
        )
        twitter_accounts_bot_detector.bom = MagicMock()
        twitter_accounts_bot_detector.bom.check_accounts_in.return_value = (
            mock_botometer_accounts_response
        )

        twitter_accounts_bot_detector.check_accounts(
            accounts_lst=MOCK_ACCOUNTS_LST
        )
        mock_botometer.Botometer.assert_called_once()
        self.assertEqual(2, len(mock_format_is_bot_account.call_args_list))

    def test_format_is_bot_account(self):
        """Test that accounts are formatted as expected."""
        for i, (screen_name, result) in enumerate(
            mock_botometer_accounts_response
        ):
            formatted_response = (
                TwitterAccountsBotDetector.format_is_bot_account(
                    screen_name=screen_name, result=result
                )
            )
            self.assertDictEqual(
                formatted_response, formatted_is_bot_accounts[i]
            )

    def test_missing_data_in_result(self):
        """Test an exception is raised when data is missing from result."""
        screen_name, result = mock_botometer_accounts_response[0]
        del result["raw_scores"]
        with self.assertRaises(Exception) as ctx:
            TwitterAccountsBotDetector.format_is_bot_account(
                screen_name=screen_name, result=result
            )
        self.assertEqual(
            f"Missing data for account {screen_name}", str(ctx.exception)
        )

    @patch(
        f"{lib_to_patch}.botometer",
    )
    def test_verify_max_botometer_requests(self, mock_botometer):
        """Verify exception is raised if we exceed limit of requests."""
        accounts_lst = MOCK_ACCOUNTS_LST * 10
        mock_botometer.Botometer = MagicMock()
        twitter_accounts_bot_detector = TwitterAccountsBotDetector(
            botometer_api=mock_botometer.Botometer
        )
        with self.assertRaises(MaxBotAccountsPerRequets) as ctx:
            twitter_accounts_bot_detector.check_accounts(
                accounts_lst=accounts_lst
            )
        self.assertIn("Max accounts per request", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
