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

    def process(self, data):
        """
        Method to process data after getting a record
        """
        return self._apply_data_transformations(data)

    def _apply_data_transformations(self, data):
        """
        Method to apply data transformations
        """
        transformer = TransformerService.get_transformer(
            implementation=f"Table:{self.table.table_name}"
        )

        if not transformer:
            return list(data.values())

        if not isinstance(data, list):
            return transformer.transform([data])[0]

        return transformer.transform(data)
