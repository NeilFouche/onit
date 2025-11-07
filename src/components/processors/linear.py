"""
Data Transformer - Linear
"""

from components.processors import Processor
from services.processing import TransformationService


@TransformationService.register_processor("Linear")
class LinearProcesor(Processor):

    def transform(self, *args, **kwargs):
        data = args[0]
        return data
