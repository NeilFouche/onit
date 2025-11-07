"""
Data transformer - FAQ

Source: FAQ
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('Get:Faq')
class FaqProcessor(Processor):
    """
    Transformer for FAQ data

    Purpose: Formatting
    Context: Getting data from the database table: FAQ
    """

    def transform(self, data, *args, **kwargs):
        faq_data = []
        for faq in data:
            faq_data.append({
                'id': faq.id,
                'key': faq.key,
                'question': faq.question,
                'answer': faq.answer,
            })

        return faq_data
