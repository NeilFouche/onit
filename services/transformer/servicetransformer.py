"""
Data transformer - Service

Source: Service
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Service')
class ServiceTransformer(TransformerService):
    """
    Transformer for service data

    Used by: Front - Service data
    """

    def transform(self, data, *args, **kwargs):
        service_data = []
        for service in data:
            service_data.append({
                "id": service.id,
                "key": service.key,
                "label": service.label,
                "description": service.description,
                "path": service.path,
                "featured": service.featured,
                "inforce": service.inforce
            })

        return service_data
