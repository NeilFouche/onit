"""
Data transformer - Path definitions

Source: Path definitions
Target: Frontend
"""

from libs.strings import to_camel_case
from services.transformer import TransformerService


@TransformerService.register_implementation('paths')
class PathsTransformer(TransformerService):
    """
    Transformer for path definitions

    Used by: Front - Menu at the bottom of all pages except the landing page
    """

    def transform(self, data):
        paths = {}
        for page in data:
            if page.children.exists():
                child_paths = {"root": page.path}
                for child in page.children.filter(active=True):
                    child_paths[to_camel_case(child.title)] = child.path
                paths[to_camel_case(page.title)] = child_paths
            else:
                paths[to_camel_case(page.title)] = page.path

        return paths
