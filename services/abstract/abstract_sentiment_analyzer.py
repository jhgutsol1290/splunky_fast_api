"""Sentiment analyzer abstract."""

from abc import ABC, abstractmethod
from typing import Dict


class SentimentAnalyzer(ABC):

    """Sentiment analyzer abstract class"""

    @classmethod
    @abstractmethod
    def analyze_sentiment(cls) -> Dict:
        """Perform sentiment analysis."""

    @staticmethod
    def get_sentiment_analysis() -> str:
        """Get sentiment classification base on the score"""
