"""Tweet utils."""
from typing import Dict


LANG = "en"
COUNT = 10
TWEET_MODE = "extended"


def format_search_tweets_keywords() -> Dict:
    """Formats the kweyword args to be used when searching tweets.

    Returns
    -------
    `Dict`
        Formatted keyword Dict
    """
    return {
        "lang": LANG,
        "count": COUNT,  # Max deafult number is 100
        "tweet_mode": TWEET_MODE,
    }


def line_breaks_to_spaces(text: str) -> str:
    """Replaces line breaks with spaces.
    
    Parameters
    ----------
    text: `str`
        Text to replace line breaks with spaces.

    Returns:
    --------
    `str`
        String updated with spaces.
    """
    return text.replace("\n", " ")
