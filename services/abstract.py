"""
Abstract base class for services.
"""

from abc import ABC, abstractmethod

class Service(ABC):
    """
    Abstract base class for services.
    """

    @abstractmethod
    def register(label):
        """Decorator to register an implementation."""
        pass