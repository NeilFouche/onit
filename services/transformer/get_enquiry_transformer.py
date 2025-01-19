"""
Data transformer - Enquiry

Source: Enquiry data
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Enquiry')
class EnquiryTransformer(TransformerService):
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
