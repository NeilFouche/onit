"""
Data transformer - Service

Source: Service
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Service')
class ServiceProcessor(Processor):
    """
    Transformer for service data

    Purpose: Formatting
    Context: Getting data from the database table: Service
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
