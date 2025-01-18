"""
Data transformer - SocialPlatform

Source: SocialPlatform
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:SocialPlatform')
class SocialPlatformTransformer(TransformerService):
    """
    Transformer for social platform data

    Used by: Front - Social platform data
    """

    def transform(self, data, *args, **kwargs):
        social_platform_data = []
        for platform in data:
            social_platform_data.append({
                'id': platform.id,
                'key': platform.key,
                'label': platform.label,
                'slug': platform.slug,
                'url': platform.url,
                'active': platform.active
            })

        return social_platform_data
