"""
Data Transformer - Client

Source: Client
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Client')
class ClientTransformer(TransformerService):
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
