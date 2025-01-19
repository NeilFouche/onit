"""
Data Transformer - Page

Source: Page
"""

from services.rest import RestService
from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Page')
class PageTransformer(TransformerService):
    """
    Transformer for page data

    Purpose: Formatting
    Context: Getting data from the database table: Page
    """

    def transform(self, data, hash_key, *args, **kwargs):
        transformer = TransformerService.get_transformer("Get:Page")

        context = RestService.get_context(hash_key)
        if context:
            transformer = TransformerService.get_transformer(context)
            return transformer.transform(data)

        page_data = []
        for page in data:
            page_data.append({
                "id": page.id,
                "title": page.title,
                "path": page.path,
                "cover_url": page.cover_url,
                "menu": page.menu,
                "active": page.active,
                "parent": transformer.transform([page.parent]) if page.parent else None
            })

        return page_data
