"""
Data Transformer - Role

Source: Role
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Role')
class RoleTransformer(TransformerService):
    """
    Transformer for role data

    Used by: Front - Role data
    """

    def transform(self, data, *args, **kwargs):
        reporting_structure_transformer = TransformerService.get_transformer(
            implementation='Table:ReportingStructure'
        )
        functional_area_transformer = TransformerService.get_transformer(
            implementation='Table:FunctionalArea'
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
