"""
Data transformer - New Enquiry Notification

Source: Request Quote/Information Form
Target: Email notification body
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Communication:Email:New:Enquiry:Transformer')
class NewEnquiryCommunicationTransformer(TransformerService):
    """
    Transformer for new enquiry email notification
    """

    def transform(self, data, *args, **kwargs):
        return "\n".join([
            "A new enquiry was added with the following details:",
            f"Name: {data.name}",
            f"Email: {data.email}",
            "----------------------------------------------",
            f"Services: {data.services}",
            f"Company: {data.company}",
            f"Message: {data.message}",
            "",
            "Please respond to this enquiry as soon as possible.",
            "",
            "Regards",
            "On It Communications Team"
        ])
