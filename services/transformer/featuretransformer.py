"""
Data transformer - Feature

Source: Feature
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Feature')
class FeatureTransformer(TransformerService):
    """
    Transformer for feature data

    Used by: Front - Feature data
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
