"""
TableCreatePostProcessor Implementation

This class is responsible for executing logic that follows the creation of a record in a table.

Post-processing logic includes:
    * Verifies dependency integrity
        Where applicable:
        * Creates dependent records
            * Includes versioning records
    * Sends notifications to the appropriate channels
        Where applicable (if notifications are enabled for this create operation):
        * Gets the applicable user groups
        * Gets the applicable template
        * Sends the notification
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor("Table:Create")
class TableCreatePostProcessor(Processor):
    """
    Concrete class - TableCreatePostProcessor Implementation
    """

    def transform(self, data, request_key=None):
        """
        Method to process data after creating a record
        """

        return data
