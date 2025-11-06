"""
TableGetPostProcessor Implementation

This class is responsible for executing logic that follows the retrieval of a record from a table.

Post-processing logic includes:
    * Applies data transformations
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor("Get:Base")
class TableGetPostProcessor(Processor):
    """
    Concrete class - TableGetPostProcessor Implementation
    """

    def __init__(self, *args, **kwargs):
        self.table = kwargs.get("table", None)

    def transform(self, request_key=None, *args, **kwargs):
        """
        Method to process data after getting a record
        """
        return args[0]
