"""
Abstract Base Class for Data Loaders
"""

from abc import ABC, abstractmethod
from typing import Any

class Source(ABC):

    def __init__(self, label = "") -> None:
        self.label = label

    @abstractmethod
    def fetch(self, request_key: str) -> Any:
        """Fetches data from the source"""