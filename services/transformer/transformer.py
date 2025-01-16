"""
On It Transformer Service

Handles data transformers

Transformers:
    Front data requests:
        - EmployeeTransformer
        - EnquiryTransformer
        - EntityFeatureTransformer
        - EntityMediaTransformer
        - FaqTransformer
        - FeatureTransformer
        - FooterMenuTransformer
        - HeaderMenuTransformer
        - MediaAssetTransformer
        - OfficeTransformer
        - PathsTransformer
        - ProjectTransformer
        - ServiceMethodTransformer
        - SegmentTransformer
        - ServiceTransformer
        - SocialPlatformTransformer
    Between tables:
        - Parameter:EntityState:Transformer
    Communication Templates:
        - Communication:Email:New:Enquiry:Transformer
"""

from abc import ABC, abstractmethod
from services.dependency import DependencyService


###############################################################################
#                            TRANSFORMER INTERFACE                            #
###############################################################################


class TransformerService(ABC):
    """ Abstract class (interface)"""

    transformer_implementations = {}

    @staticmethod
    def register_implementation(label):
        """
        Decorator to dynamically register a transformer class in the `transformers` dictionary.
        """
        def decorator(cls):
            TransformerService.transformer_implementations[label] = cls()
            return cls
        return decorator

    @staticmethod
    def get_transformer(implementation):
        """Transformer factory"""
        if implementation not in TransformerService.transformer_implementations:
            DependencyService.load_registered_implementations(
                parent=TransformerService, package='services/transformer'
            )

        if implementation not in TransformerService.transformer_implementations:
            return None

        return TransformerService.transformer_implementations[implementation]

    @abstractmethod
    def transform(self, data):
        """Default behavior (returns data as-is)"""
        return data
