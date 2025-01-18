"""
Data Transformer - Client

Source: Client
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Client')
class ClientTransformer(TransformerService):
    """
    Transformer for client data

    Used by: Front - Client data
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
