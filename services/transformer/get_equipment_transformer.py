"""
Data Transformer - Equipment

Source: Equipment
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Equipment')
class EquipmentTransformer(TransformerService):
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
