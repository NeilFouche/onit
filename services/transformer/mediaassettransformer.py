"""
Data transformer - MediaAsset

Source: MediaAsset
Target: Frontend
"""

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from libs.strings import kebab_to_camel
from services.database import DatabaseService
from services.transformer import TransformerService
from services.rest import RestService


@TransformerService.register_implementation('Table:MediaAsset')
class MediaAssetTransformer(TransformerService):
    """
    Transformer for entity media data

    Used by: Front - Entity media data
    """

    def transform(self, data, hash_key, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        entity_media_set = onitdb.entity_media.get_queryset(
            hash_key, reset=False
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
        } for media in entity_media_set if media.media_asset] if entity_media_set else None

        if media_asset_data:
            onitdb.entity_media.set_queryset(hash_key, queryset=None)
            return media_asset_data

        transformer = TransformerService.get_transformer(
            implementation='Table:MediaAsset:RelatedReduced'
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
