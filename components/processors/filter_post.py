"""
TableFilterPostProcessor Implementation

This class is responsible for executing logic that follows the filtering of a table.

Post-processing logic includes:
    * Applies data transformations
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor("Filter:Base")
class TableFilterPostProcessor(Processor):
    """
    Concrete class - TableFilterPostProcessor Implementation
    """

    def __init__(self, *args, **kwargs):
        self.table = kwargs.get("table", None)

    def transform(self, request_key=None, *args, **kwargs):
        """
        Method to process data after filtering a table
        """
        # Remove record linked to inactive entities (if applicable)
        return args[0]
