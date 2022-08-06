"""Test Vader sentiment analyzer module."""
from typing import Dict
import unittest
from unittest.mock import patch

from services.sentiment_analyzer.vader_sentiment_analyzer import (
    VaderSentimentAnylyzer,
)

lib_to_patch = "services.sentiment_analyzer.vader_sentiment_analyzer"


def make_vader_response(compund: float) -> Dict:
    """Util function to create Vader responses."""
    return {"neg": 0.0, "neu": 0.585, "pos": 0.415, "compound": compund}


class TestVaderSentimentAnalyzer(unittest.TestCase):

    """Test Vader Sentiment Analyzer module."""

    def setUp(self) -> None:
        """SetUp."""
        self.text = "Test text"

    @patch(
        f"{lib_to_patch}.SentimentIntensityAnalyzer.polarity_scores",
        return_value=make_vader_response(compund=0.5),
    )
    @patch(
        f"{lib_to_patch}.VaderSentimentAnylyzer.get_sentiment_analysis",
        return_value="positive",
    )
    def test_analyze_sentiment(
        self, mock_get_sentiment_analysis, mock_polarity_scores
    ):
        """Test analyze sentiment method."""
        res = VaderSentimentAnylyzer.analyze_sentiment(text=self.text)
        expected_res = {
            "sentiment_score": 0.5,
            "sentiment_classification": "positive",
        }
        mock_polarity_scores.assert_called_once_with(text=self.text)
        mock_get_sentiment_analysis.assert_called_once_with(score=0.5)
        self.assertDictEqual(res, expected_res)

    def test_get_sentiment_analysis(self):
        """Test function to return the expected value."""
        expected_res = "positive"
        res = VaderSentimentAnylyzer.get_sentiment_analysis(score=0.8)

        self.assertEqual(expected_res, res)

        expected_res = "neutral"
        res = VaderSentimentAnylyzer.get_sentiment_analysis(score=0.0)

        self.assertEqual(expected_res, res)

        expected_res = "negative"
        res = VaderSentimentAnylyzer.get_sentiment_analysis(score=-0.8)

        self.assertEqual(expected_res, res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
