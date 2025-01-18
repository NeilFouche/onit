"""
Data transformer - Footer

Source: Footer
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('footer')
class FooterMenuTransformer(TransformerService):
    """
    Transformer for footer menu

    Used by: Front - Menu at the bottom of all pages except the landing page
    """

    def transform(self, data, *args, **kwargs):
        nav_data = []
        for page in data:
            nav_data.append({
                "subheader": page.title,
                "items": [{
                    "title": child.title,
                    "path": child.path,
                } for child in page.children.filter(menu="footer", active=True)] if page.children.exists() else None
            })

        return nav_data
