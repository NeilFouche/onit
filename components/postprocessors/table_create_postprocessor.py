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

from components.postprocessors import PostProcessor
from components.version_control.history import History
from services.configuration import ConfigurationService
from services.database import DatabaseService
from services.transformer import TransformerService
from services.communication import CommunicationService


@PostProcessor.register_implementation("Table:Create")
class TableCreatePostProcessor(PostProcessor):
    """
    Concrete class - TableCreatePostProcessor Implementation
    """

    def __init__(self, table):
        self.table = table

    def process(self, data, hash_key=None):
        """
        Method to process data after creating a record
        """
        self._version_control(data)
        self._verify_dependency_integrity(data)
        self._send_notifications(data)

        return data

    def _version_control(self, data):
        """
        Method to version control
        """
        # Check if versioning is enabled
        versioning_config = ConfigurationService.get_parameter(
            category="Versioning", key=self.table.model_name
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
        onitdb = DatabaseService.get_database()
        dependencies = self._get_dependencies()
        if not dependencies:
            return

        for dependency in dependencies:
            transformer = TransformerService.get_transformer(
                implementation=f"{self.table.model_name}:{dependency}:Transformer"
            )
            if not transformer:
                continue

            data = transformer.transform(data)
            dependent_table = onitdb.get_table(dependency)
            dependent_table.create(data)

    def _get_dependencies(self):
        """
        Method to get dependencies
        """
        return ConfigurationService.get_parameter(
            category="Dependencies",
            key=self.table.model_name
        )

    def _send_notifications(self, data):
        """
        Method to send notifications

        If notification is enabled for this create operation:
            - Get the applicable meta data
            - Send the notification
        """
        new_notification = ConfigurationService.get_parameter(
            category="Communication", key=f"SendNotification:New:{self.table.model_name}"
        )
        if not new_notification:
            return

        CommunicationService.notify(
            configuration=new_notification, data=data
        )
