"""
Data transformer - SocialPlatform

Source: SocialPlatform
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:SocialPlatform')
class SocialPlatformProcessor(Processor):
    """
    Transformer for social platform data

    Purpose: Formatting
    Context: Getting data from the database table: Social platform
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
