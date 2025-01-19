"""
TableFilterPostProcessor Implementation

This class is responsible for executing logic that follows the filtering of a table.

Post-processing logic includes:
    * Applies data transformations
"""

from components.postprocessors import PostProcessor
from services.transformer import TransformerService


@PostProcessor.register_implementation("Table:Get:MultipleRecords")
class TableFilterPostProcessor(PostProcessor):
    """
    Concrete class - TableFilterPostProcessor Implementation
    """

    def __init__(self, table):
        self.table = table

    def process(self, data, hash_key=None):
        """
        Method to process data after filtering a table
        """
        # Remove record linked to inactive entities (if applicable)
        data = self._remove_inactive_entities(data)

        return self._apply_data_transformations(data, hash_key)

    def _apply_data_transformations(self, data, hash_key):
        """
        Method to apply data transformations
        """
        transformer = TransformerService.get_transformer(
            implementation=f"Get:{self.table.model_name}"
        )

        if not transformer:
            return list(data.values())

        return transformer.transform(data, hash_key)

    def _remove_inactive_entities(self, data):
        """
        Method to remove records linked to inactive entities
        """
        if hasattr(self.table, '_active'):
            return data.filter(active=True)

        if hasattr(self.table, '_inforce'):
            return data.filter(inforce=True)

        return data
