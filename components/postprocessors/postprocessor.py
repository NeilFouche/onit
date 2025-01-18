"""
Postprocessor Interface
"""

from abc import ABC, abstractmethod
from services.dependency import DependencyService


class PostProcessor(ABC):
    """ Abstract class (interface)"""

    processor_implementations = {}

    def __init__(self, table):
        self.table = table

    @staticmethod
    def register_implementation(label):
        """
        Method that registers the postprocessor class for the specified label
        """
        def decorator(cls):
            PostProcessor.processor_implementations[label] = cls
            return cls
        return decorator

    @staticmethod
    def get_processor(implementation, table):
        """Postprocessor factory"""

        if implementation not in PostProcessor.processor_implementations:
            DependencyService.load_registered_implementations(
                parent=PostProcessor, package='components/postprocessors'
            )

        if implementation not in PostProcessor.processor_implementations:
            return None

        return PostProcessor.processor_implementations[implementation](table)

    @ abstractmethod
    def process(self, data, hash_key):
        """Method to process data"""
