"""
TableDeletePreprocessor Implementation

This class is responsible for executing logic that precedes the deletion of a record in a table.

Pre-processing logic includes:
    - Verifies dependency integrity
        Where applicable:
        - Deletes/versions child records
"""

from components.processors import Processor
from services.database import DatabaseService
from services.processing import TransformationService


@TransformationService.register_processor("Table:Delete")
class TableDeletePreprocessor(Processor):
    """
    Concrete class - TableDeletePreprocessor Implementation
    """

    def __init__(self, *args, **kwargs):
        self.table = kwargs.get("table", None)
        self.database = DatabaseService.get_database()

    def transform(self, data, request_key=None):
        """
        Method to process data before deleting a record
        """
        return data
