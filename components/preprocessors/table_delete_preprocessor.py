"""
TableDeletePreprocessor Implementation

This class is responsible for executing logic that precedes the deletion of a record in a table.

Pre-processing logic includes:
    - Verifies dependency integrity
        Where applicable:
        - Deletes/versions child records
"""

from components.preprocessors import PreProcessor
from services.database import DatabaseService
from services.configuration import ConfigurationService
from services.transformer import TransformerService


@PreProcessor.register_implementation("Table:Delete")
class TableDeletePreprocessor(PreProcessor):
    """
    Concrete class - TableDeletePreprocessor Implementation
    """

    def __init__(self, table):
        self.table = table
        self.database = DatabaseService.get_database()

    def process(self, data, hash_key=None):
        """
        Method to process data before deleting a record
        """
        self._verify_dependency_integrity(data)

    def _verify_dependency_integrity(self, data):
        """
        Method to verify dependency integrity
        """
        dependencies = self._get_dependencies()
        for dependency in dependencies:
            transformer = TransformerService.get_transformer(
                implementation=f"{self.table.name}To{dependency}DeleteTransformer"
            )
            data = transformer.transform(data)
            dependent_table = self.database.get_table(dependency)
            dependent_table.delete(data)

    def _get_dependencies(self):
        """
        Method to get dependencies
        """
        return ConfigurationService.get_parameter(
            category="Dependencies",
            key=self.table.name
        )
