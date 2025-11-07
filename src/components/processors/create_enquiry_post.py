"""
EnquiryCreatePostProcessor Implementation

This class is responsible for executing logic that follows the creation of a record in a table.

Post-processing logic includes:
    * Create EntityFeature records
        * Use provisional records stored on the table class to create the EntityFeature records
        * Remove the provisional records
    * Sends notifications to the appropriate channels
        Where applicable (if notifications are enabled for this create operation):
        * Load the configuration for the notification
        * Get the transformer name
        * Use transformer to get the resolved content for the notification
        * Pass the data to CommunicationService to send the notification
"""

from components.processors import Processor
from services.configuration import ConfigurationService
from services.database import DatabaseService
from services.processing import TransformationService
from services.communication import CommunicationService


@TransformationService.register_processor("Create:Enquiry:Post")
class EnquiryCreatePostProcessor(Processor):
    """
    Concrete class - EnquiryCreatePostProcessor Implementation
    """

    def __init__(self):
        onitdb = DatabaseService.get_database()
        self.table = onitdb.enquiry

    def transform(self, data, request_key=None):
        """
        Method to process data after creating a record
        """
        services = self.create_entity_features(data, request_key)
        data["services"] = services

        self._send_notifications(data)

        return data

    def create_entity_features(self, data, request_key):
        """
        Method to create EntityFeature records

        Note: Services is a required field on the frontend so at this point
        it should be in the data.
        """

        return data

    def _send_notifications(self, data):
        """
        Method to send notifications

        If notification is enabled for this create operation:
            - Get the applicable meta data
            - Send the notification
        """
        new_notification = ConfigurationService.get_parameter(
            category="Communication", key=f"Notification:New:{self.table.model_name}"
        )

        if not new_notification:
            return

        CommunicationService.notify(
            configuration=new_notification, data=data
        )
