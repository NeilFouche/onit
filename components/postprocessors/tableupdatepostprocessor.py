"""
TableUpdatePostProcessor Implementation

This class is responsible for executing logic that follows the update of a record in a table.

Post-processing logic includes:
    * Version control
        Where applicable:
        * Creates versioning records
    * Verifies dependency integrity
        Where applicable:
        * Creates dependent records
            * Includes versioning records
    * Sends notifications to the appropriate channels
        Where applicable (if notification is enabled for this create operation):
        * Gets the applicable user groups
        * Gets the applicable template
        * Sends the notification
    * Applies data transformations
        * Gets the applicable transformer
        * Applies the transformation
"""

from components.postprocessors import PostProcessor
from components.version_control.history import History
from services.database import DatabaseService
from services.configuration import ConfigurationService
from services.transformer import TransformerService
from services.communication import CommunicationService


@PostProcessor.register_implementation("Table:Update")
class TableUpdatePostProcessor(PostProcessor):
    """
    Concrete class - TableUpdatePostProcessor Implementation
    """

    def __init__(self, table):
        self.table = table
        self.database = DatabaseService.get_database()

    def process(self, data, hash_key=None):
        """
        Method to process data after updating a record
        """
        self._version_control(data)
        self._verify_dependency_integrity(data)
        self._send_notifications(data)

        return self._apply_data_transformations(data, hash_key)

    def _apply_data_transformations(self, data, hash_key):
        """
        Method to apply data transformations
        """
        transformer = TransformerService.get_transformer(
            implementation=f"Table:{self.table.name}"
        )

        if not transformer:
            return list(data.values())

        if not isinstance(data, list):
            return transformer.transform([data], hash_key)[0]

        return transformer.transform(data, hash_key)

    def _version_control(self, data):
        """
        Method to version control
        """
        # Check if versioning is enabled
        versioning_config = ConfigurationService.get_parameter(
            category="Versioning", key=self.table.name
        )
        if not versioning_config:
            return

        # Create versioning records
        entity_state = self.table.create_state()
        entity_history = History(data)
        entity_history.push(entity_state)

    def _verify_dependency_integrity(self, data):
        """
        Method to verify dependency integrity
        """
        dependencies = self._get_dependencies()
        for dependency in dependencies:
            transformer = TransformerService.get_transformer(
                implementation=f"{self.table.name}To{dependency}UpdateTransformer"
            )
            if not transformer:
                continue

            data = transformer.transform(data)
            dependent_table = self.database.get_table(dependency)
            dependent_table.create(data)

    def _get_dependencies(self):
        """
        Method to get dependencies
        """
        return ConfigurationService.get_parameter(
            category="Dependencies",
            key=self.table.name
        )

    def _send_notifications(self, data):
        """
        Method to send notifications

        If notification is enabled for this update operation:
            - Get the applicable meta data
            - Send the notification
        """
        notification_config = ConfigurationService.get_parameter(
            category="Communication", key=f"SendNotification:Update:{self.table.name}"
        )
        if not notification_config:
            return

        communication_meta = notification_config.get("meta", "Default")
        CommunicationService.notify(
            meta=communication_meta, data=data
        )
