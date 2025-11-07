"""
Data Transformer - Client

Source: Client
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Client')
class ClientProcessor(Processor):
    """
    Transformer for client data

    Purpose: Formatting
    Context: Getting data from the database table: Client
    """

    def transform(self, data, *args, **kwargs):
        client_data = []
        for client in data:
            client_data.append({
                "id": client.id,
                "key": client.key,
                "slug": client.slug,
                "label": client.label,
                "contact": client.contact,
                "office": client.office,
                "phone": client.phone,
                "industry": client.industry
            })

        return client_data
