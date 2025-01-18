"""
Data Transformer - FunctionalArea

Source: FunctionalArea
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:FunctionalArea')
class FunctionalAreaTransformer(TransformerService):
    """
    Transformer for functional_area data

    Used by: Front - FunctionalArea data
    """

    def transform(self, data, *args, **kwargs):
        functional_area_data = []
        for functional_area in data:
            functional_area_data.append({
                "id": functional_area.id,
                "key": functional_area.key,
                "label": functional_area.label,
                "description": functional_area.description,
                "code": functional_area.code
            })

        return functional_area_data
