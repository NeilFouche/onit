"""
Data transformer - Header Menu

Source: Header menu data
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor('header')
class HeaderMenuProcessor(Processor):
    """
    Transformer for header menu

    Purpose: Formatting
    Context: Getting data from the database table: Menu at the top of the page
    """

    def transform(self, data, *args, **kwargs):
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
