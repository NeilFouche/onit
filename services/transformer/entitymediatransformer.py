"""
Data transformer - EntityMedia

Source: EntityMedia
Target: Frontend
"""

from services.database import DatabaseService
from services.transformer import TransformerService


@TransformerService.register_implementation('Table:EntityMedia')
class EntityMediaTransformer(TransformerService):
    """
    Transformer for entity media data

    Used by: Front - Entity media data
    """

    def transform(self, data, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        entity_media_data = []
        for entity_media in data:
            related_table = onitdb.get_table_from_type(
                content_type_id=entity_media["content_type_id"]
            )
            related_entity = related_table.get(pk=entity_media["object_id"])
            media_asset = entity_media.get("media_asset", None)

            if not related_entity and not media_asset:
                continue

            entity_media_data.append({
                'model': related_table.model_name if related_table else None,
                'entity_key': related_table.key if related_table else None,
                'entity_label': str(related_entity) if related_entity else None,
                'media_asset_key': media_asset.key if media_asset else None,
                'media_asset_label': media_asset.label if media_asset else None,
                'type': media_asset.category if media_asset else None
            })

            return entity_media_data
