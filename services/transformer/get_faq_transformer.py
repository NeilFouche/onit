"""
Data transformer - FAQ

Source: FAQ
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Faq')
class FaqTransformer(TransformerService):
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
