"""
Data transformer - New Enquiry Notification

Source: Request Quote/Information Form
Target: Email notification body
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Communication:New:Enquiry')
class NewEnquiryCommunicationProcessor(Processor):
    """
    Transformer for new enquiry email notification
    """

    def transform(self, data, *args, **kwargs):
        return "\n".join([
            "A new enquiry was added with the following details:",
            "",
            f"Name: {data.get('first_name', '')} {data.get('last_name', '')}",
            f"Email: {data.get('email', '')}",
            f"Phone: {data.get('phone', '')}",
            "----------------------------------------------",
            f"Services: {', '.join(data.get('services'))}",
            f"Company: {data.get('company', '')}",
            f"Message: {data.get('message', '')}",
            "",
            "Please respond to this enquiry as soon as possible.",
            "",
            "Regards",
            "On It Communications Team"
        ])
