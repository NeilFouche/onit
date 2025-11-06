"""
Data Transformer - ReportingStructure

Source: ReportingStructure
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:ReportingStructure')
class ReportingStructureProcessor(Processor):
    """
    Transformer for reporting_structure data

    Purpose: Formatting
    Context: Getting data from the database table: ReportingStructure
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
