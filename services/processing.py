

from components.processors import Processor
from libs.discovery import load_registered_implementations
from services import Service

class TransformationService(Service):
    """
    Service for managing data transformations and processing.
    """

    processors: dict[str, Processor] = {}

    @staticmethod
    def get_processor(implementation: str) -> Processor:
        """
        Returns a processor instance based on the processor name.
        """
        if implementation not in TransformationService.processors:
            load_registered_implementations(package_name="components.processors")

        fallback_processor = TransformationService.processors['Linear']
        if implementation not in TransformationService.processors:
            processor_type = implementation.split(":", 1)[0]
            fallback_processor = TransformationService.processors.get(f"{processor_type}:Base", fallback_processor)

        return TransformationService.processors.get(implementation, fallback_processor)

    @staticmethod
    def register_processor(label):
        """
        Decorator to register a processor class.
        """
        def decorator(cls):
            TransformationService.processors[label] = cls()
            return cls
        return decorator