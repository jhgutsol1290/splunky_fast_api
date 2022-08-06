"""Sentiment analyzer implementation."""


from typing import Dict

from services.abstract.abstract_sentiment_analyzer import SentimentAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class VaderSentimentAnylyzer(SentimentAnalyzer):
    """Sentiment Analyzer implementation using Vader.

    See Vader docs https://pypi.org/project/vaderSentiment/
    """

    @classmethod
    def analyze_sentiment(cls, text: str) -> Dict:
        """Analyze text sentiment.

        Parameters
        ----------
        text: `str`
            Text to analyze sentiment.

        Returns
        -------
        `dict`
            Text, sentiment classification and score.
        """
        return {
            "sentiment_score": (
                score := SentimentIntensityAnalyzer().polarity_scores(
                    text=text
                )["compound"]
            ),
            "sentiment_classification": cls.get_sentiment_analysis(
                score=score
            ),
        }

    @staticmethod
    def get_sentiment_analysis(score: float) -> str:
        """Get the sentiment classification based on a score.

        Parameters
        ----------
        score: `float`
            Score obtained from the SentimentAnalyzer library.

        Returns
        -------
        `str`:
            Sentiment classification
                'positive' -> score >= 0.05
                'neutral' -> score between -0.05 and 0.05
                'negative' -> score <= -0.05
        """
        match score:
            case _ if score >= 0.05:
                sentiment_classification = "positive"
            case _ if score <= -0.05:
                sentiment_classification = "negative"
            case _ if score < 0.05 or score > -0.05:
                sentiment_classification = "neutral"
        return sentiment_classification
