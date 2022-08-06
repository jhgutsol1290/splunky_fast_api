"""Abstract Data retirever."""

from abc import ABC, abstractmethod
from typing import Dict, List


class DataCollector(ABC):

    """Abstract DataCollector class."""

    @abstractmethod
    def get_data_by_single_query(self, query: str) -> List[Dict]:
        """Get data based on a specific keyword."""
