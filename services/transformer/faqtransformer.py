"""
Data transformer - FAQ

Source: FAQ
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Faq')
class FaqTransformer(TransformerService):
    """
    Transformer for FAQ data

    Used by: Front - FAQ data
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
