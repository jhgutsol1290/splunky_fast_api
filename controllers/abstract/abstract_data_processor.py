"""Abstract Data Processor module."""

from abc import ABC, abstractmethod


class SentimentDataProcessor(ABC):

    """Data processor abstract class."""

    @abstractmethod
    def get_data(self, *args, **kwargs) -> None:
        """Get main data from data collector."""

    @abstractmethod
    def analyze_sentiment_data(self) -> None:
        """Perform sentiment analyzer to data."""

    @abstractmethod
    async def get_data_to_db(self) -> None:
        """Gets the data to the DB."""

    @abstractmethod
    async def process_data(self, *args, **kwargs) -> bool:
        """Process all data."""
