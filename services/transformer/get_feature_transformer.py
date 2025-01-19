"""
Data transformer - Feature

Source: Feature
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Feature')
class FeatureTransformer(TransformerService):
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
