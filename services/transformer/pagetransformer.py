"""
Data Transformer - Page

Source: Page
Target: Frontend
"""

from services.rest import RestService
from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Page')
class PageTransformer(TransformerService):
    """
    Transformer for page data

    Used by: Front - Page data
    """

    def transform(self, data):
        transformer = TransformerService.get_transformer("Table:Page")

        context = RestService.get_context()
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
