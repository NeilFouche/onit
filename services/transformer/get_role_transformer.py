"""
Data Transformer - Role

Source: Role
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Role')
class RoleTransformer(TransformerService):
    """
    Transformer for role data

    Purpose: Formatting
    Context: Getting data from the database table: Role
    """

    def transform(self, data, *args, **kwargs):
        reporting_structure_transformer = TransformerService.get_transformer(
            implementation='Get:ReportingStructure'
        )
        functional_area_transformer = TransformerService.get_transformer(
            implementation='Get:FunctionalArea'
        )

        role_data = []
        for role in data:
            role_data.append({
                "id": role.id,
                "key": role.key,
                "label": role.label,
                "description": role.description,
                "code": role.code,
                "reporting_level": reporting_structure_transformer.transform([role.reporting_level]),
                "functional_area": functional_area_transformer.transform([role.functional_area])
            })

        return role_data
