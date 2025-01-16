"""
Serializers for Django Rest Framework (DRF)
"""

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import (
    Body,
    BodyItem,
    Employee,
    Enquiry,
    EntityFeature,
    EntityMedia,
    Feature,
    MediaAsset,
    Office,
    Region,
    Segment,
    Service,
    ServiceMethod
)


class BodyItemSerializer(serializers.ModelSerializer):
    """Serializer for BodyItem records"""
    class Meta:
        model = BodyItem
        fields = ['id', 'key', 'value', 'description', 'body']


class BodySerializer(serializers.ModelSerializer):
    """Serializer for Body records"""
    items = BodyItemSerializer(many=True, read_only=True)

    class Meta:
        model = Body
        fields = ['id', 'key', 'label', 'description', 'segment', 'items']


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee records"""
    person = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'key', 'email', 'phone',
                  'hire_date', 'person', 'role']

    def get_person(self, obj):
        return str(obj.person)

    def get_role(self, obj):
        return str(obj.role)


class EnquirySerializer(serializers.ModelSerializer):
    """Serializer for Enquiry records"""
    services = serializers.ListField(
        child=serializers.CharField(), write_only=True)

    class Meta:
        model = Enquiry
        fields = ['id', 'key', 'label', 'first_name', 'last_name', 'email',
                  'phone', 'company', 'website', 'message', 'created_at', 'services']
        read_only_fields = ['key', 'label']

    def create(self, validated_data):
        """Create Enquiry and related EntityFeature records"""
        services = validated_data.pop('services')
        enquiry = Enquiry.objects.create(**validated_data)

        # Create related EntityFeature records
        content_type = ContentType.objects.get_for_model(Enquiry)
        features = Feature.objects.filter(label__in=services)
        for feature in features:
            EntityFeature.objects.create(
                feature=feature, content_type=content_type, object_id=enquiry.id)

        return enquiry


class EntityFeatureSerializer(serializers.ModelSerializer):
    """Serializer for EntityFeature records"""

    model_name = serializers.CharField(
        source='content_type.model', read_only=True
    )
    entity_key = serializers.CharField(
        source='entity.key', read_only=True
    )
    entity_label = serializers.CharField(
        source='entity', read_only=True
    )
    feature_key = serializers.CharField(
        source='feature.key', read_only=True
    )
    feature_label = serializers.CharField(
        source='feature.label', read_only=True
    )
    entity = serializers.SerializerMethodField()

    class Meta:
        model = EntityFeature
        fields = [
            'model_name',
            'entity_key',
            'entity_label',
            'feature_key',
            'feature_label',
            'object_id',
            'entity'
        ]

    def get_entity(self, obj):
        """Returns a string representation of the entity"""
        serializer_class = SERIALIZER_MAPPING.get(type(obj.entity))
        if serializer_class:
            return serializer_class(obj.entity, context=self.context).data
        return None


class EntityMediaSerializer(serializers.ModelSerializer):
    """Serializer for EntityMedia records"""
    model_name = serializers.CharField(
        source='entity._meta.model_name', read_only=True
    )
    entity_key = serializers.CharField(
        source='entity.key', read_only=True
    )
    entity_label = serializers.CharField(
        source='entity', read_only=True
    )
    media_asset_key = serializers.CharField(
        source='media_asset.key', read_only=True
    )
    media_asset_label = serializers.CharField(
        source='media_asset.label', read_only=True
    )
    type = serializers.CharField(
        source='media_asset.category', read_only=True
    )

    class Meta:
        model = EntityMedia
        fields = [
            'model_name',
            'entity_key',
            'entity_label',
            'media_asset_key',
            'media_asset_label',
            'type',
            'object_id'
        ]


class MediaAssetSerializer(serializers.ModelSerializer):
    """Serializer for MediaAsset records"""

    class Meta:
        model = MediaAsset
        fields = ['id', 'key', 'label', 'slug', 'description', 'credit',
                  'format', 'relative_path', 'width', 'height', 'category']


class OfficeSerializer(serializers.ModelSerializer):
    """Serializer for Office records"""

    class Meta:
        model = Office
        fields = ['id', 'key', 'label', 'area', 'email',
                  'address', 'phone', 'head', 'headoffice']


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for Region records"""

    class Meta:
        model = Region
        fields = ['id', 'key', 'label', 'slug', 'description',
                  'capital', 'population']


class SegmentSerializer(serializers.ModelSerializer):
    """Serializer for Segment records"""
    body = BodySerializer(read_only=True)

    class Meta:
        model = Segment
        fields = ['id', 'key', 'label', 'type', 'featured', 'context', 'body']


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service records"""

    class Meta:
        model = Service
        fields = ['id', 'key', 'label', 'description',
                  'path', 'featured', 'inforce', 'last_update']


class ServiceMethodSerializer(serializers.ModelSerializer):
    """Serializer for Service records"""
    service_id = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = ServiceMethod
        fields = ['id', 'key', 'label', 'description', 'path', 'featured', 'inforce',
                  'last_update', 'service_id', 'target_id']

    def get_service_id(self, obj):
        """Returns a string representation of the entity"""
        return obj.service.id if obj.service else None

    def get_target_id(self, obj):
        """Returns a string representation of the entity"""


SERIALIZER_MAPPING = {
    Employee: EmployeeSerializer,
    Enquiry: EnquirySerializer,
    MediaAsset: MediaAssetSerializer,
    Office: OfficeSerializer,
    Region: RegionSerializer,
    Segment: SegmentSerializer,
    Service: ServiceSerializer,
    ServiceMethod: ServiceMethodSerializer
}
