"""
Data transformer - EnquiryFeature

Source: EnquiryFeature
Target: EnquiryCreate PreProcessor
"""

from django.contrib.contenttypes.models import ContentType
from components.processors import Processor
from services.database import DatabaseService
from services.processing import TransformationService


@TransformationService.register_processor('Create:EnquiryFeature')
class EnquiryFeatureProcessor(Processor):
    """
    Transformer for entity feature data

    Used by: EnquiryCreatePreProcessor
    """

    def transform(self, services, *args, **kwargs):
        onitdb = DatabaseService.get_database()
        content_type = ContentType.objects.get(pk=onitdb.enquiry.content_type_id)

        enquiry_feature_data = {}
        for service in services:
            onitdb.feature.filter({"key": service}).first()

            enquiry_feature_data[service] = {
                'feature': onitdb.feature.id,
                'content_type': content_type,
                "object_id": None,
            }

        return enquiry_feature_data
