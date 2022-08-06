"""HTTP utils for tweets module."""

from fastapi import HTTPException

from models.enums import SentimentClassificationEnum


def verify_hashtag(hashtag_query: str) -> None:
    """Verifies if the input hashtag is valid.

    Parameters
    ----------
    hashtag_query: `Dict`
        Input hashtag query string.

    Returns
    -------
    `None`

    Raises
    ------
    `HttpException`
    """
    if any(
        [
            not hashtag_query,
            not hashtag_query.startswith("#"),
            len(hashtag_query.split(" ")) > 1,
        ]
    ):
        raise HTTPException(
            status_code=500,
            detail="Hashtag (#) is required and should be only one.",
        )


def verify_valid_classificator(sentiment_classificator: str):
    """Verify if the inout classificator is valid.

    Paramters
    ---------
    sentiment_classificator: `str`
        Sentiment classificator to filter data with.

    Returns
    -------
    `None`

    Raises
    ------
    `HttpException`
    """
    if sentiment_classificator not in (
        item.value for item in SentimentClassificationEnum
    ):
        raise HTTPException(
            status_code=500,
            detail="Not a valid sentiment classificator",
        )
