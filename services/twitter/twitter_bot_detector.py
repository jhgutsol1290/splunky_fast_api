"""Twitter bot account detector."""

import json
from typing import Dict, List

import botometer
from decouple import config
from services.twitter.authentication import TwitterAuthenticatorData
from utils.decorators.custom_decorators import verify_max_botometer_requests

rapidapi_key = config("RAPIDAPI_KEY")

IS_BOT_SCORE = 0.6


class TwitterAccountsBotDetector:
    """Tweet Bots detector class."""

    def __init__(self, botometer_api: botometer.Botometer) -> None:
        """Init method.

        Consider that we have only 500 requests per day.
        See: https://github.com/IUNetSci/botometer-python
        """
        self.bom = botometer_api(
            wait_on_ratelimit=True,
            rapidapi_key=rapidapi_key,
            **TwitterAuthenticatorData().dict(),
        )

    @verify_max_botometer_requests
    def check_accounts(self, *, accounts_lst: List[str]) -> List[Dict]:
        """Verify if the accounts are bots based on Botometer library.

        Parameters
        ----------
        accounts_lst: `List[str]`
            List of accounts to verify. Account should have @, i.e @elonmusk

        Returns
        -------
        `List[Dict]`:
            Accounts with botometer score.
        """
        accounts_verified = [
            self.format_is_bot_account(screen_name=screen_name, result=result)
            for screen_name, result in self.bom.check_accounts_in(
                accounts=accounts_lst
            )
        ]
        print(json.dumps(accounts_verified, indent=4))
        return accounts_verified

    @staticmethod
    def format_is_bot_account(screen_name: str, result: Dict) -> Dict:
        """Format Is Twitter bot account.

        if score >= 0.6 account is likely to be a bot.
        if score < 0.6 account is likely to be a real account.

        Parameters
        ----------
        screen_name: `str`
            Twitter screen_name.

        result: `Dict`
            Complete result of the botometer calculation

        Returns
        -------
        `Dict`
            Formatted response.

        Raises
        ------
        `Exception`
            Missing data.
        """
        print("Result ==== ")
        print(json.dumps(result, indent=4))

        try:
            return {
                "user_screen_name": screen_name,
                "botometer_score": (
                    botometer_score := result["raw_scores"]["english"][
                        "overall"
                    ]
                ),
                "is_bot": botometer_score >= IS_BOT_SCORE,
            }
        except KeyError as e:
            raise Exception(f"Missing data for account {screen_name}") from e


# result = bom.check_account("@ScaryCommie1917") #!Bot account


if __name__ == "__main__":
    TwitterAccountsBotDetector(
        botometer_api=botometer.Botometer
    ).check_accounts(accounts_lst=["@elonmusk", "@ScaryCommie1917"])
