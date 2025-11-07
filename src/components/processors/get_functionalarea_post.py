"""
Data Transformer - FunctionalArea

Source: FunctionalArea
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:FunctionalArea')
class FunctionalAreaProcessor(Processor):
    """
    Transformer for functional_area data

    Purpose: Formatting
    Context: Getting data from the database table: FunctionalArea
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
