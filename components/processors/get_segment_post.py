"""
Data transformer - Segment

Source: Segment
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Segment')
class SegmentProcessor(Processor):
    """
    Transformer for segment data

    Purpose: Formatting
    Context: Getting data from the database table: Segment
    """

    def transform(self, data, *args, **kwargs):
        segment_data = []
        for segment in data:
            segment_data.append({
                'id': segment.id,
                'key': segment.key,
                'label': segment.label,
                'type': segment.type,
                'featured': segment.featured,
                'context': segment.context,
                'body': {
                    'id': segment.body.id,
                    'items': [
                        {
                            'id': item.id,
                            'key': item.key,
                            'value': item.value,
                            'description': item.description,
                        }
                        for item in segment.body.items.all()
                    ],
                } if hasattr(segment, 'body') else None
            })

        return segment_data
