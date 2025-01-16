"""
TableCreatePreprocessor Implementation

This class is responsible for executing logic the precedes the creation of a record in a table.

Pre-processing logic includes:
    - Remove invalid fields
"""

from components.preprocessors import PreProcessor


@PreProcessor.register_implementation("Table:Create")
class TableCreatePreprocessor(PreProcessor):
    """
    Concrete class - TableCreatePreprocessor Implementation
    """

    def __init__(self, table):
        self.table = table

    def process(self, data):
        """
        Method to process data before creating a record
        """
        self._remove_invalid_fields(data)

    def _remove_invalid_fields(self, data):
        """
        Method to remove invalid fields
        """
        for key in list(data.keys()):
            if key not in self.table.get_field_names():
                data.pop(key)
