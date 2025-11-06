"""
Data Transformer - Page

Source: Page
"""

from components.processors import Processor
from services.rest import RestService
from services.processing import TransformationService


@TransformationService.register_processor('Get:Page')
class PageProcessor(Processor):
    """
    Transformer for page data

    Purpose: Formatting
    Context: Getting data from the database table: Page
    """

    def transform(self, data, request_key, *args, **kwargs):
        transformer = TransformationService.get_processor("Get:Page")

        if request_key is None:
            raise ValueError(f"Request key is required for processing Page data.")

        context = RestService.get_context(request_key)
        if context:
            transformer = TransformationService.get_processor(context)
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
