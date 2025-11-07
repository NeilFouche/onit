"""
Data Transformer - Equipment

Source: Equipment
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Equipment')
class EquipmentProcessor(Processor):
    """
    Transformer for equipment data

    Purpose: Formatting
    Context: Getting data from the database table: Equipment
    """

    def transform(self, data, *args, **kwargs):
        equipment_data = []
        for equipment in data:
            equipment_data.append({
                "id": equipment.id,
                "label": equipment.label,
                "serial": equipment.serial,
                "description": equipment.description
            })

        return equipment_data
