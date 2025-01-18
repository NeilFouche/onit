"""
Data transformer - Segment

Source: Segment
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Segment')
class SegmentTransformer(TransformerService):
    """
    Transformer for segment data

    Used by: Front - Segment data
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
