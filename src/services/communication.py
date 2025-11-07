"""
On It Communication Service

Handles sending notifications to recipients.

Communication media:
 - Email
"""

from django.core.mail import send_mail
from services.database import DatabaseService
from services.processing import TransformationService


class CommunicationService:
    """
    Handles sending notifications to recipients
    """
    @staticmethod
    def send_email(subject, message, recipient_list, sender="admin@onitafrica.com"):
        """
        Method to send an email
        """
        if not isinstance(recipient_list, list):
            recipient_list = list(recipient_list)

        if not sender:
            sender = "admin@onitafrica.com"

        try:
            send_mail(
                subject=subject,
                message=message,
                recipient_list=recipient_list,
                from_email=sender,
                fail_silently=False
            )
        except Exception as err:
            print(f"Email failed: {err}")
            raise

    @staticmethod
    def notify(configuration, data):
        """
        Method to send notifications to the recipient groups
        """
        # Resolve the message
        transformer_name = configuration.get("transformer")
        transformer = TransformationService.get_processor(transformer_name)
        message = transformer.transform(data) if transformer else ""

        # Set recipient list
        recipient_groups = configuration.get("recipient_groups")
        onitdb = DatabaseService.get_database()
        onitdb.group.set_queryset(
            request_key="Notification:New:Enquiry",
            filter_params={"name__in": recipient_groups},
            reset=True
        )
        groups = onitdb.group.get_queryset("Notification:New:Enquiry")
        recipient_list = [
            user.email for group in groups for user in group.user_set.all()
        ]

        # Send the email
        subject = configuration.get("subject", "")
        sender = configuration.get("sender", None)
        CommunicationService.send_email(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            sender=sender
        )
