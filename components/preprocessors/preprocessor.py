"""
Pre-processor Interface
"""

from abc import ABC, abstractmethod
from services.dependency import DependencyService


class PreProcessor(ABC):
    """ Abstract class (interface)"""

    processor_implementations = {}

    @staticmethod
    def register_implementation(label):
        """
        Method that registers the preprocessor class for the specified label
        """
        def decorator(cls):
            PreProcessor.processor_implementations[label] = cls
            return cls
        return decorator

    @staticmethod
    def get_processor(implementation, table):
        """Preprocessor factory"""
        if implementation not in PreProcessor.processor_implementations:
            DependencyService.load_registered_implementations(
                parent=PreProcessor, package='components/preprocessors'
            )

        if implementation not in PreProcessor.processor_implementations:
            return None

        return PreProcessor.processor_implementations[implementation](table)

    @abstractmethod
    def process(self, data, hash_key=None):
        """Method to process data"""
