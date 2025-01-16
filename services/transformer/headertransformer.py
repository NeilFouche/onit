"""
Data transformer - Header Menu

Source: Header menu data
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('header')
class HeaderMenuTransformer(TransformerService):
    """
    Transformer for header menu

    Used by: Front - Menu at the top of the page
    """

    def transform(self, data):
        nav_data = []
        for page in data:
            nav_data.append({
                "title": page.title,
                "path": page.path,
                "children": [{
                    "coverUrl": child.cover_url,
                    "items": [{"title": child.title, "path": child.path}]
                } for child in page.children.filter(menu="header", active=True)] if page.children.exists() else None
            })

        return nav_data
