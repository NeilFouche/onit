"""
Data transformer - ServiceMethod

Source: ServiceMethod
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:ServiceMethod')
class ServiceMethodProcessor(Processor):
    """
    Transformer for service method data

    Purpose: Formatting
    Context: Getting data from the database table: Service method
    """

    def transform(self, data, *args, **kwargs):
        service_transformer = TransformationService.get_processor('Get:Service')
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
