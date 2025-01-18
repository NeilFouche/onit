"""
Data Transformer - ReportingStructure

Source: ReportingStructure
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:ReportingStructure')
class ReportingStructureTransformer(TransformerService):
    """
    Transformer for reporting_structure data

    Used by: Front - ReportingStructure data
    """

    def transform(self, data, *args, **kwargs):
        reporting_structure_data = []
        for reporting_structure in data:
            reporting_structure_data.append({
                "id": reporting_structure.id,
                "key": reporting_structure.key,
                "label": reporting_structure.label,
                "description": reporting_structure.description,
                "level": reporting_structure.level
            })

        return reporting_structure_data
