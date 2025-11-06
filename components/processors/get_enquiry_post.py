"""
Data transformer - Enquiry

Source: Enquiry data
"""

from components.processors import Processor

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Enquiry')
class EnquiryProcessor(Processor):
    """
    Transformer for enquiry data

    Purpose: Formatting
    Context: Getting data from the database table: Enquiry
    """

    def transform(self, data):
        enquiry_data = []
        for enquiry in data:
            enquiry_data.append({
                "id": enquiry.id,
                "key": enquiry.key,
                'label': enquiry.label,
                'first_name': enquiry.first_name,
                'last_name': enquiry.last_name,
                'email': enquiry.email,
                'phone': enquiry.phone,
                'company': enquiry.company,
                'website': enquiry.website,
                'message': enquiry.message
            })

        return enquiry_data
