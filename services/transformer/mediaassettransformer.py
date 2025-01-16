"""
Data transformer - MediaAsset

Source: MediaAsset
Target: Frontend
"""

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from libs.strings import kebab_to_camel
from services.transformer import TransformerService
from services.rest import RestService


@TransformerService.register_implementation('Table:MediaAsset')
class MediaAssetTransformer(TransformerService):
    """
    Transformer for entity media data

    Used by: Front - Entity media data
    """

    def transform(self, data):
        context = RestService.get_context()
        model_name = kebab_to_camel(context)
        related_model = apps.get_model('front', model_name)
        content_type = ContentType.objects.get_for_model(related_model)
        query_parameters = RestService.get_query_parmeters()

        media_asset_data = []
        for media in data:
            related_entity = self.select_entity(
                media, content_type, query_parameters
            )

            media_asset_data.append({
                'model': media._meta.label,
                'entity_key': related_entity.key if related_entity else None,
                'entity_label': str(related_entity) if related_entity else None,
                'media_asset_key': media.key,
                'media_asset_label': media.label,
                'type': media.category,
            })

        return media_asset_data

    def select_entity(self, media, content_type, query_parameters):
        """
        Finds the applicable entity for the media asset from requested context.
        """

        entities = list(
            media.mediaentities.filter(content_type=content_type)
        )

        if len(entities) == 1:
            return entities[0].entity

        for related_entity in entities:
            for key in query_parameters.keys():
                if getattr(related_entity.entity, key) in query_parameters[key]:
                    return related_entity.entity

        return None
