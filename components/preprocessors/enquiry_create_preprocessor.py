"""
EnquiryCreatePreprocessor Implementation

This class is responsible for executing logic the precedes the creation of a record in a table.

Pre-processing logic includes:
    - Converting field names from camelCase to snake_case (if applicable)
    - Creating EntityFeature records based on the specified services
"""

from components.preprocessors import PreProcessor
from libs.strings import camel_to_snake
from services.database import DatabaseService
from services.transformer import TransformerService


@PreProcessor.register_implementation("Enquiry:Create")
class EnquiryCreatePreProcessor(PreProcessor):
    """
    Concrete class - TableCreatePreprocessor Implementation
    """

    def __init__(self, table):
        self.table = table

    def process(self, data, hash_key=None):
        """
        Method to process data before creating a record
        """
        self.create_provisional_entity_features(data, hash_key)
        return self.sanitize_data(data)

    def create_provisional_entity_features(self, data, hash_key):
        """
        Method to create EntityFeature records

        Note: Services is a required field on the frontend so at this point it
        should be in the data.
        """
        transformer = TransformerService.get_transformer(
            implementation="Create:EnquiryFeature"
        )
        entity_feature_items = transformer.transform(data["services"])
        self.table.create_provisional_records(hash_key, entity_feature_items)

    def sanitize_data(self, data):
        """
        Converts keys in camelCase or PascalCase to snake_case and
        remove any keys that does not match the field names in the table.
        """
        new_data = {}
        for key, value in data.items():
            new_key = camel_to_snake(key)
            if new_key in self.table.field_names:
                new_data[new_key] = value

        return new_data
