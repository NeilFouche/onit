"""
Register the webste data models for maintenance in the Admin App.
"""

from django.contrib import admin

from front import models


@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'slug']
    list_editable = ['key', 'label', 'slug']


@admin.register(models.Terminology)
class TerminologyAdmin(admin.ModelAdmin):
    list_display = ['id', 'acronym', 'slug', 'label']
    list_editable = ['acronym', 'slug', 'label']


@admin.register(models.Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'type', 'context']
    list_editable = ['key', 'label', 'type', 'context']


@admin.register(models.Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'description', 'segment']
    list_editable = ['key', 'label', 'description', 'segment']


@admin.register(models.BodyItem)
class BodyItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'value', 'description', 'body']
    list_editable = ['key', 'value', 'description', 'body']


@admin.register(models.EntityMedia)
class EntityMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'media_asset', 'content_type', 'object_id']
    list_editable = ['media_asset', 'content_type', 'object_id']


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'inforce',
                    'description', 'path', 'featured']
    list_editable = ['key', 'label',
                     'description', 'path', 'inforce']


@admin.register(models.ServiceMethod)
class ServiceMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'description',
                    'featured', 'inforce', 'service', 'target']
    list_editable = ['key', 'label', 'description',
                     'featured', 'inforce', 'service', 'target']


@admin.register(models.EntityFeature)
class EntityFeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'feature', 'content_type', 'object_id']
    list_editable = ['feature', 'content_type', 'object_id']


@admin.register(models.Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'question', 'answer']
    list_editable = ['key', 'question', 'answer']


@admin.register(models.Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'area',
                    'email', 'address', 'phone', 'head', 'headoffice']
    list_editable = ['key', 'label', 'area',
                     'email', 'address', 'phone', 'head', 'headoffice']


@admin.register(models.Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'first_name', 'last_name',
                    'email', 'phone', 'company', 'website', 'message']
    list_editable = ['key', 'label', 'first_name', 'last_name',
                     'email', 'phone', 'company', 'website', 'message']


@admin.register(models.MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'slug', 'description',
                    'credit', 'format', 'relative_path', 'category']
    list_editable = ['key', 'label', 'slug', 'description',
                     'credit', 'format', 'relative_path', 'category']


@admin.register(models.Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'serial', 'label']
    list_editable = ['serial', 'label']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'key', 'label',
                    'description', 'capital', 'population']
    list_editable = ['slug', 'key', 'label',
                     'description', 'capital', 'population']


@admin.register(models.ReportingStructure)
class ReportingStructureAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'level', 'description']
    list_editable = ['key', 'label', 'level', 'description']


@admin.register(models.FunctionalArea)
class FunctionalAreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'code', 'description']
    list_editable = ['key', 'label', 'code', 'description']


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'code',
                    'reporting_level', 'functional_area']
    list_editable = ['key', 'label', 'code',
                     'reporting_level', 'functional_area']


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'email', 'phone', 'person', 'role']
    list_editable = ['key', 'email', 'person', 'role']


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'initials',
                    'title', 'date_of_birth', 'email', 'phone']
    list_editable = ['first_name', 'last_name', 'initials',
                     'title', 'date_of_birth', 'email', 'phone']


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'path', 'parent', 'menu', 'active']
    list_editable = ['title', 'path', 'parent', 'menu', 'active']


@admin.register(models.SocialPlatform)
class SocialPlatformAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'slug', 'url', 'active']
    list_editable = ['key', 'label', 'slug', 'url', 'active']


@admin.register(models.S3Bucket)
class S3BucketAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'label', 'aws_region', 'is_active']
    list_editable = ['key', 'label', 'is_active']
