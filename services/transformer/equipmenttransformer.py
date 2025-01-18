"""
Data Transformer - Equipment

Source: Equipment
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Equipment')
class EquipmentTransformer(TransformerService):
    """
    Transformer for equipment data

    Used by: Front - Equipment data
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
