"""
Data models for On It Website API
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.serializers.json import DjangoJSONEncoder


################################################################################
#                               Reference Models                               #
################################################################################


class Feature(models.Model):
    """A data model for Features"""

    key = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['label']


################################## MANAGEMENT STRUCTURE ###################################


class ReportingStructure(models.Model):
    """
    A data model for the Reporting Structure. With Functional Areas forms a management matrix.

    Codes:
     - 1: Executive Management  (Executive Management - CEO, COO, CTO, ...)
     - 2: Senior Management     (Senior Engineering Manager, Senior Business Analyst, Senior Safety Officer)
     - 3: Middle Management     (Specialists)
     - 4: First-line Management (Site Supervisor)
     - 5: Operational Staff     (Team Leader)
    """

    key = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    level = models.SmallIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['level']


class FunctionalArea(models.Model):
    """
    A data model for the Functional Areas. With Reporting Structure forms a management matrix.

    Codes:
     - E: Engineering
     - O: Operations
     - S: Safety
     - H: Human Resources
     - F: Finance
    """

    key = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=2, db_index=True)

    def __str__(self) -> str:
        return str(self.label)


################################## REGION ###################################


class Region(models.Model):
    """
    A data model for Regions

    Regions:
    - 9 Provinces
    - Africa
    """

    key = models.CharField(max_length=64, unique=True, db_index=True)
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )
    label = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    capital = models.CharField(max_length=255, null=True)
    population = models.IntegerField()

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['label']


################################### PARAMETER ####################################

class Parameter(models.Model):
    """A data model for Parameters"""

    key = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    default = models.CharField(max_length=255, null=True, blank=True)
    data_type = models.CharField(max_length=32, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    scope = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['label']


################################## TERMINOLOGY ###################################


class Terminology(models.Model):
    """A data model for Terminology"""

    acronym = models.CharField(max_length=8)
    label = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self) -> str:
        return f"{str(self.acronym).upper()} - {self.label}"

    class Meta:
        ordering = ['label']
        verbose_name_plural = 'Terminology'


################################################################################
#                              Core Entity Models                              #
################################################################################


class MediaAsset(models.Model):
    """
    A data model for media assets, like images, videos and documents

    FKs: category
    M2M: {feature: EntityFeature}
    """

    key = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )
    description = models.TextField(null=True, blank=True)
    credit = models.CharField(max_length=255, null=True, blank=True)
    format = models.CharField(max_length=6)
    relative_path = models.CharField(max_length=511, null=True, blank=True)
    filesize = models.IntegerField(null=True, blank=True)
    timestamp = models.FloatField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['category', 'label']


################################## SERVICES & SERVICE METHODS ###################################


class Service(models.Model):
    """
    A data model for services

    M2M = {icon: EntityMedia, cover: EntityMedia}
    """

    key = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    inforce = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        When activating or deactivating a service, the website should respond to the update
        by no longer displaying the service (when it is deactivated) and vice versa.
        """
        if self.pk is not None:
            # Compare the current 'inforce' status with the new one
            previous_inforce = Service.objects.filter(
                pk=self.pk).values_list('inforce', flat=True).first()

            if previous_inforce != self.inforce:
                Page.objects.filter(title=self.label).update(
                    active=self.inforce)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['label']


class ServiceMethod(models.Model):
    """
    A data model for service methods

    FKs: service, target
    M2M = {icon: EntityMedia}
    """

    key = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    inforce = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="methods"
    )
    target = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="targets"
    )

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['service', 'label']


################################## OFFICE & OFFICE HOURS ###################################


class Office(models.Model):
    """
    A data model for Offices

    M2M = {cover: EntityMedia}
    """

    key = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    area = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=24, null=True, blank=True)
    head = models.CharField(max_length=255)
    headoffice = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['label']


class OperatingHours(models.Model):
    """
    A data model for Office Hours
    """

    class DayOfWeek(models.TextChoices):
        MONDAY = 'MON', 'Monday'
        TUESDAY = 'TUE', 'Tuesday'
        WEDNESDAY = 'WED', 'Wednesday'
        THURSDAY = 'THU', 'Thursday'
        FRIDAY = 'FRI', 'Friday'
        SATURDAY = 'SAT', 'Saturday'
        SUNDAY = 'SUN', 'Sunday'

    day_of_week = models.CharField(
        max_length=3,
        choices=DayOfWeek.choices
    )
    office = models.ForeignKey(
        Office,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="operatinghourdays"
    )
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('office', 'day_of_week')
        ordering = ['office', 'day_of_week']
        verbose_name_plural = 'Office hours'


################################## EQUIPMENT ###################################


class Equipment(models.Model):
    """A data model for Equipment"""

    serial = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['label']
        verbose_name_plural = 'Equipment'


################################## QUESTIONS & QUESTIONNAIRES ###################################


class Faq(models.Model):
    """A data model for FAQs"""

    key = models.CharField(max_length=64, unique=True, db_index=True)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self) -> str:
        return str(self.key)

    class Meta:
        ordering = ['key']



################################## SEGMENTS ###################################


class Segment(models.Model):
    """
    A data model for Segments

    A segment is a part of a webpage that may contain images, text or other media.
    In addition to the fields of this model, a segment may or may not contain a body
    that defines additional content of the segment.
    """

    key = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(max_length=255, db_index=True, null=True)
    type = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    context = models.CharField(max_length=32, db_index=True)

    def __str__(self) -> str:
        return str(self.label)


class Body(models.Model):
    """
    A data model for Segment Bodies

    A body defines additional content to display in a segment. The body record itself contains
    basic information about the content. Each body can have 0, 1 or multiple BodyItems that
    adds specific content for just this body instance.
    """

    key = models.CharField(max_length=64, unique=True, db_index=True)
    label = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )
    description = models.TextField(null=True, blank=True)
    segment = models.OneToOneField(
        Segment,
        on_delete=models.CASCADE,
        related_name='body'
    )

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        verbose_name_plural = 'Bodies'


class BodyItem(models.Model):
    """A data model for BodyItems"""

    key = models.CharField(max_length=64, db_index=True)
    value = models.CharField(max_length=3072, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    body = models.ForeignKey(
        Body,
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True
    )

    def __str__(self) -> str:
        return str(self.id)  # type: ignore

    class Meta:
        ordering = ['id']


################################## ENQUIRY ###################################


class Enquiry(models.Model):
    """A data model for Enquiries"""

    key = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=128, db_index=True)
    first_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True
    )
    last_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True
    )
    email = models.EmailField()
    phone = models.CharField(max_length=24, null=True, blank=True)
    company = models.CharField(max_length=64, null=True, blank=True)
    website = models.CharField(max_length=128, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Automatically set the key and label
        """

        if not self.key:
            self.key = "enq-onit"

        if not self.label:
            full_name = f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else ""
            self.label = f"Enquiry: {full_name} {self.email}"

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        ordering = ['email']
        verbose_name_plural = 'Enquiries'


################################## ROLE ###################################


class Role(models.Model):
    """A data model for Roles"""

    key = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=4, db_index=True)
    reporting_level = models.ForeignKey(
        ReportingStructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roles'
    )
    functional_area = models.ForeignKey(
        FunctionalArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roles'
    )

    def __str__(self) -> str:
        return str(self.label)

    class Meta:
        ordering = ['reporting_level', 'code']


################################## PERSON ###################################


class Person(models.Model):
    """
    A data model for Persons

    email: Personal email address
    """

    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    initials = models.CharField(max_length=10)
    title = models.CharField(max_length=6)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=24, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


################################## EMPLOYEE ###################################


class Employee(models.Model):
    """
    A data model for Employees

    email: Email given on domain onitafrica.com - only exists for an employee and if applicable.
    phone: Work number if applicable
    """

    key = models.CharField(max_length=64, db_index=True)
    email = models.EmailField(null=True, blank=True, db_index=True)
    phone = models.CharField(max_length=24, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="employee"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="employees"
    )

    def __str__(self) -> str:
        return str(self.person)

    class Meta:
        ordering = ['role']


################################## PAGE - NAVIGATION ###################################


class Page(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    path = models.CharField(max_length=255)
    cover_url = models.CharField(max_length=500, blank=True, null=True)
    menu = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    def __str__(self):
        return f"{self.title} - {self.menu}"

    class Meta:
        ordering = ['menu', 'id']


class SocialPlatform(models.Model):
    """A data model for SocialPlatforms"""

    key = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)
    url = models.CharField(max_length=500)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.label)


###############################################################################
#                  Relationship Models (Intermediate Tables)                  #
###############################################################################


class EntityFeature(models.Model):
    """A data model for Entity Features

    For characterizing an entity, i.e. assigning an attribute to an entity
    that may be unique to an individual entity or a select amount of entities.
    """

    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="featureentities"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="entityfeatures"
    )
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ('content_type', 'object_id', 'feature')


################################## ENTITY MEDIA ###################################


class EntityMedia(models.Model):
    """A data model for Entity Media

    For linking media assets (videos, images, web addresses, documents)
    to an entity (segment, service, person, ...)
    """

    media_asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name="mediaentities"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="entitymedia"
    )
    object_id = models.PositiveIntegerField(db_index=True)
    entity = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = 'Entity media'