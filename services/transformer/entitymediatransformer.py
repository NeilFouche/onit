"""
Data transformer - EntityMedia

Source: EntityMedia
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:EntityMedia')
class EntityMediaTransformer(TransformerService):
    """
    Transformer for entity media data

    Used by: Front - Entity media data
    """

    def transform(self, data):
        entity_media_data = []
        for entity_media in data:
            if entity_media.media_asset:
                entity_media_data.append({
                    'model': entity_media.entity._meta.label,
                    'entity_key': entity_media.entity.key,
                    'entity_label': str(entity_media.entity),
                    'media_asset_key': entity_media.media_asset.key,
                    'media_asset_label': entity_media.media_asset.label,
                    'type': entity_media.media_asset.category,
                })
