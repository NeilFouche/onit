"""
Data transformer - Office

Source: Office
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Office')
class OfficeTransformer(TransformerService):
    """
    Transformer for office data

    Used by: Front - Office data
    """

    def transform(self, data):
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
