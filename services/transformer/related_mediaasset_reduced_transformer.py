"""
Data transformer - EntityMedia

Source: EntityMedia
"""

from services.database import DatabaseService
from services.transformer import TransformerService


@TransformerService.register_implementation('Get:MediaAsset:RelatedReduced')
class EntityMediaTransformer(TransformerService):
    """
    Transformer for entity media data

    Purpose: Formatting
    Context: Getting data from the database table: EntityMedia
    """

    def transform(self, data, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        entity_media_data = []
        for entity_media in data:
            related_table = onitdb.get_table_from_type(
                content_type_id=entity_media["content_type_id"]
            )
            if related_table:
                entity_media_data.append(related_table.model_name)

        return entity_media_data
