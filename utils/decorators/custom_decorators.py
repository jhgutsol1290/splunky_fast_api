"""Custom decorators module."""
from typing import Callable, Dict, List

from utils.custom_exceptions.twitter_exceptions import (
    HashtagRequiredException,
    MaxBotAccountsPerRequets,
)


MAX_BOT_ACCOUNTS_PER_REQUEST = 5


def single_hashtag_validator(function: Callable[[str], List[Dict]]):
    """Decorator function to make hashtag required.

    Parameters
    ----------
    function: `Callable`
        Function to be decorated.

    Returns
    -------
    `List[Dict]`
    """

    def wrapper(*args, **kwargs) -> List[Dict]:
        hashtag_query = kwargs.get("query", "")
        if any(
            [
                not hashtag_query,
                not hashtag_query.startswith("#"),
                len(hashtag_query.split(" ")) > 1,
            ]
        ):
            raise HashtagRequiredException(
                "Hashtag (#) is required and should be only one."
            )
        return function(*args, **kwargs)

    return wrapper


def verify_max_botometer_requests(function: Callable[[List[str]], List[Dict]]):
    """Verify accounts len are less than the allowed limit per request.

    Parameters
    ----------
    function: `Callable`
        Function to be decorated.

    Returns
    -------
    `List[Dict]`
    """

    def wrapper(*args, **kwargs) -> List[Dict]:
        if len(kwargs.get("accounts_lst", [])) > MAX_BOT_ACCOUNTS_PER_REQUEST:
            raise MaxBotAccountsPerRequets(
                f"Max accounts per request is -> {MAX_BOT_ACCOUNTS_PER_REQUEST}"
            )
        return function(*args, **kwargs)

    return wrapper
