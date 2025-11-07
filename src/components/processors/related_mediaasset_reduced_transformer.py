"""
Data transformer - EntityMedia

Source: EntityMedia
"""

from components.processors import Processor
from services.database import DatabaseService
from services.processing import TransformationService


@TransformationService.register_processor('Get:MediaAsset:RelatedReduced')
class EntityMediaProcessor(Processor):
    """
    Transformer for entity media data

    Purpose: Formatting
    Context: Getting data from the database table: EntityMedia
    """

    def transform(self, data, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        entity_media_data = []
        for entity_media in data:
            related_table = onitdb.get(content_type_id=entity_media["content_type_id"])
            if related_table:
                entity_media_data.append(related_table.model_name)

        return entity_media_data
