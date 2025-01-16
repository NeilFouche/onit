"""
On It Communication Service

Handles sending notifications to recipients.

Communication media:
 - Email
"""

from django.core.mail import send_mail
from services.transformer import TransformerService


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
    def notify(meta, data):
        """
        Method to send notifications to the recipient groups
        """
        recipient_groups = meta.get("recipient_groups", [])
        sender = meta.get("sender", "")

        transformer_name = meta.get("transformer", None)
        transformer = TransformerService.get_transformer(transformer_name)
        message = transformer.transform(data) if transformer else ""

        subject = meta.get("subject", "").replace(
            "{{enquiry.key}}", data.get("key", "")
        )

        for group in recipient_groups:
            CommunicationService.send_email(
                subject=subject,
                message=message,
                recipient_list=group,
                sender=sender
            )
