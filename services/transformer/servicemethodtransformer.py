"""
Data transformer - ServiceMethod

Source: ServiceMethod
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:ServiceMethod')
class ServiceMethodTransformer(TransformerService):
    """
    Transformer for service method data

    Used by: Front - Service method data
    """

    def transform(self, data):
        service_transformer = TransformerService.get_transformer(
            'Table:Service')
        service_method_data = []
        for service_method in data:
            service_method_data.append({
                "id": service_method.id,
                "key": service_method.key,
                "label": service_method.label,
                "description": service_method.description,
                "path": service_method.path,
                "featured": service_method.featured,
                "inforce": service_method.inforce,
                "service": service_transformer.transform([service_method.service]),
                "target": service_transformer.transform([service_method.target])
            })

        return service_method_data
