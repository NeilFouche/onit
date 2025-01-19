"""
TableGetPostProcessor Implementation

This class is responsible for executing logic that follows the retrieval of a record from a table.

Post-processing logic includes:
    * Applies data transformations
"""

from components.postprocessors import PostProcessor
from services.transformer import TransformerService


@PostProcessor.register_implementation("Table:Get:SingleRecord")
class TableGetPostProcessor(PostProcessor):
    """
    Concrete class - TableGetPostProcessor Implementation
    """

    def __init__(self, table):
        self.table = table

    def process(self, data, hash_key=None):
        """
        Method to process data after getting a record
        """
        return self._apply_data_transformations(data, hash_key)

    def _apply_data_transformations(self, data, hash_key):
        """
        Method to apply data transformations
        """
        transformer = TransformerService.get_transformer(
            implementation=f"Get:{self.table.table_name}"
        )

        if not transformer:
            return self.table.__dict__

        if not isinstance(data, list):
            return transformer.transform([data], hash_key)[0]

        return transformer.transform(data, hash_key)
