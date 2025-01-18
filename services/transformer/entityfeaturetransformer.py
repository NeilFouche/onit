"""
Data transformer - EntityFeature

Source: EntityFeature
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:EntityFeature')
class EntityFeatureTransformer(TransformerService):
    """
    Transformer for entity feature data

    Used by: Front - Entity feature data
    """

    def transform(self, data, *args, **kwargs):
        entity_feature_data = []
        for entity_feature in data:
            entity_feature_data.append({
                'model': entity_feature.content_object._meta.label,
                'feature_key': entity_feature.feature.key,
                'feature_label': entity_feature.feature.label,
                "entity_key": entity_feature.content_object.key,
                'entity': {
                    "label": entity_feature.content_object.label if hasattr(entity_feature.content_object, 'label') else None,
                    "category": entity_feature.content_object.category if hasattr(entity_feature.content_object, 'category') else None,
                    "width": entity_feature.content_object.width if hasattr(entity_feature.content_object, 'width') else None,
                    "height": entity_feature.content_object.height if hasattr(entity_feature.content_object, 'height') else None
                }
            })

        return entity_feature_data
