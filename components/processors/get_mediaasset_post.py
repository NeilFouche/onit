"""
Data transformer - MediaAsset

Source: MediaAsset
"""

from components.processors import Processor
from services.database import DatabaseService
from services.processing import TransformationService


@TransformationService.register_processor('Get:MediaAsset')
class MediaAssetProcessor(Processor):
    """
    Transformer for entity media data

    Purpose: Formatting
    Context: Getting data from the database table: Entity media
    """

    def transform(self, data, request_key, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        entity_media_set = onitdb.entity_media.get_queryset(
            request_key, reset=False
        )

        media_asset_data = [{
            'model': media._meta.label,
            'entity_key': media.entity.key,
            'entity_label': str(media.entity),
            'media_asset_key': media.media_asset.key,
            'media_asset_label': media.media_asset.label,
            'type': media.media_asset.category,
            'width': media.media_asset.width,
            'height': media.media_asset.height
        } for media in entity_media_set if media.media_asset] if entity_media_set else []

        if media_asset_data:
            onitdb.entity_media.set_queryset(request_key, queryset=None)
            return self.deduplicate(media_asset_data)

        transformer = TransformationService.get_processor(
            implementation='Get:MediaAsset:RelatedReduced'
        )

        return [{
            'model': media._meta.label,
            'entities': transformer.transform(media.mediaentities.values()),
            'media_asset_key': media.key,
            'media_asset_label': media.label,
            'type': media.category,
            'width': media.width,
            'height': media.height
        } for media in data]

    def deduplicate(self, data):
        unique_data = {}
        for item in data:
            hashable_key = tuple(item.items())
            if hashable_key not in unique_data:
                unique_data[hashable_key] = item

        return list(unique_data.values())