"""
Data transformer - EnquiryFeature

Source: EnquiryFeature
Target: EnquiryCreate PreProcessor
"""

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from services.database import DatabaseService
from services.transformer import TransformerService


@TransformerService.register_implementation('Create:EnquiryFeature')
class EnquiryFeatureTransformer(TransformerService):
    """
    Transformer for entity feature data

    Used by: EnquiryCreatePreProcessor
    """

    def transform(self, services, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        enquiry = apps.get_model('api', 'Enquiry')
        content_type = ContentType.objects.get_for_model(enquiry)

        enquiry_feature_data = {}
        for service in services:
            feature = onitdb.feature\
                .filter({"key": service}, processor=None)\
                .first()

            enquiry_feature_data[service] = {
                'feature': feature.id,
                'content_type': content_type,
                "object_id": None,
            }

        return enquiry_feature_data
