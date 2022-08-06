"""Requests schemas."""

from enum import Enum
from schemas.base import HashtagBase
from pydantic import validator


class HashtagIn(HashtagBase):
    """HashtagIn schema."""

    @validator("query")
    def validate_query(cls, value):
        try:
            if len(value.split(" ")) == 1 and value.startswith("#"):
                return value
            raise ValueError("Hashtag (#) is required and should be only one.")
        except Exception as e:
            raise ValueError(
                "Hashtag (#) is required and should be only one."
            ) from e


class SentimentClassificatorIn(str, Enum):
    """SentimentClassificatorIn schema."""
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
