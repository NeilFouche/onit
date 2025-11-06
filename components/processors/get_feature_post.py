"""
Data transformer - Feature

Source: Feature
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Feature')
class FeatureProcessor(Processor):
    """
    Transformer for feature data

    Purpose: Formatting
    Context: Getting data from the database table: Feature
    """

    def transform(self, data, *args, **kwargs):
        feature_data = []
        for feature in data:
            feature_data.append({
                'id': feature.id,
                'key': feature.key,
                'label': feature.label,
                'slug': feature.slug,
                'description': feature.description,
            })

        return feature_data
