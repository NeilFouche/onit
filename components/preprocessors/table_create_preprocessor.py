"""
TableCreatePreprocessor Implementation

This class is responsible for executing logic the precedes the creation of a record in a table.

Pre-processing logic includes:
    - Remove invalid fields
"""

from components.preprocessors import PreProcessor
from libs.strings import camel_to_snake


@PreProcessor.register_implementation("Table:Create")
class TableCreatePreprocessor(PreProcessor):
    """
    Concrete class - TableCreatePreprocessor Implementation
    """

    def __init__(self, table):
        self.table = table

    def process(self, data, hash_key=None):
        """
        Method to process data before creating a record
        """
        return self.sanitize_data(data)

    def sanitize_data(self, data):
        """
        Converts keys in camelCase or PascalCase to snake_case and
        remove any keys that does not match the field names in the table.
        """
        new_data = {}
        for key, value in data.items():
            new_key = camel_to_snake(key)
            if new_key in self.table.field_names:
                new_data[new_key] = value

        return new_data
