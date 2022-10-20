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


def count_hashtags(data: list) -> dict:
    """Counts hashtags in tweets.
    
    Parameters
    ----------
    data: `list`
        List of tweet objects.

    Returns:
    --------
    `dict`
        Dictionary with the count by hashtag.
    """
    hashtag_count_dict = {}
    for item in data:
        hashtag = item.title
        if hashtag not in hashtag_count_dict.keys():
            hashtag_count_dict[hashtag] = 1
        else:
            hashtag_count_dict[hashtag] += 1
    return hashtag_count_dict