"""
Data Transformer - Parameter

Source: Parameter
"""

import json

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Parameter')
class ParameterProcessor(Processor):
    """
    Transformer for parameter data

    Purpose: Formatting
    Context: Getting data from the database table: Parameter
    """

    def transform(self, data, *args, **kwargs):
        parameter_data = []
        for parameter in data:
            parameter_data.append({
                "id": parameter.id,
                "key": parameter.key,
                "slug": parameter.slug,
                "description": parameter.description,
                "value": json.loads(parameter.value) if "{" in parameter.value else parameter.value,
                "default": parameter.default,
                "data_type": parameter.data_type,
                "category": parameter.category,
                "scope": parameter.scope
            })

        return parameter_data
