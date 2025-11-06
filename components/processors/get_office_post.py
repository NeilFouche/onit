"""
Data transformer - Office

Source: Office
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Office')
class OfficeProcessor(Processor):
    """
    Transformer for office data

    Purpose: Formatting
    Context: Getting data from the database table: Office
    """

    def transform(self, data, *args, **kwargs):
        office_data = []
        for office in data:
            office_data.append({
                'id': office.id,
                'key': office.key,
                'label': office.label,
                'area': office.area,
                'email': office.email,
                'address': office.address,
                'phone': office.phone,
                'head': office.head,
                'headoffice': office.headoffice
            })

        return office_data
