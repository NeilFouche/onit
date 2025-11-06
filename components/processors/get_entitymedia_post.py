"""
Data transformer - EntityMedia

Source: EntityMedia
"""

from components.processors import Processor
from services.database import DatabaseService
from services.processing import TransformationService


@TransformationService.register_processor('Get:EntityMedia')
class EntityMediaProcessor(Processor):
    """
    Transformer for entity media data

    Purpose: Formatting
    Context: Getting data from the database table: Entity media
    """

    def transform(self, data, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        entity_media_data = []
        for entity_media in data:
            related_table = onitdb.get(content_type_id=entity_media["content_type_id"])
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
