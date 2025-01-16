"""
Data Transformer - Parameter

Source: Parameter
Target: Frontend
"""

import json
from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Parameter')
class ParameterTransformer(TransformerService):
    """
    Transformer for parameter data

    Used by: Front - Parameter data
    """

    def transform(self, data):
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
