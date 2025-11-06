"""
Database Table Wrapper

Handles table operations.
"""

import json
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models, connection
from django.forms.models import model_to_dict
from typing import cast, Type, TypeVar, Optional

from onit.constants import EMPTY_QUERYSET
from components.dataclasses import TableField

T = TypeVar("T", bound=models.Model)

class Table:
    """A wrapper class for relational database tables"""

    def __init__(self, table_name, db_table_name, model: Optional[Type[T]]):
        self.table_name = table_name
        self.__model_name: str = ""
        self.__db_table_name: str = db_table_name
        self.__data_model: Optional[Type[models.Model]] = model
        self.__field_names = []
        self.__fields = []
        self._querysets = {}
        self.id = 0
        self.key = ""
        self.content_type_id = 0

        self.dependent_table = ""
        self.foreign_keys = {}
        self.neighbours = {}
        self.table_type = ""
        self.weight = 1

        self._initialize()

    ###########################################################################
    #                          DATABASE INTERACTIONS                          #
    ###########################################################################

    def create(self, item: dict) -> int:
        """Creates an record in the database"""
        if not self.data_model:
            raise ValueError(f"Cannot create new record for table {self.table_name} because its data model does not exist.")

        new_instance = self.data_model.objects.create(**item)

        if new_instance:
            self._populate_fields(model_to_dict(new_instance))

        return self.id


    def get(self, *args, **kwargs) -> Optional[models.Model]:
        """
        Gets a record from the database.

        Args:
            - 1 positional argument (optional, int): Assumed as the primary key
            - Any number of keyword arguments: Fields to filter on

        Returns:
            Model: The model instance.
        """
        if not self.data_model:
            return None

        if args and 'pk' not in kwargs:
          kwargs['pk'] = args[0]

        instance = self.data_model.objects.filter(**kwargs).first()
        if not instance:
            return None

        self._populate_fields(model_to_dict(instance))

        return instance


    def filter(self, query = {}, request_key = None, use_current = True, **kwargs) -> models.QuerySet:
        """
        Gets multiple records from the database.

        Args:
            query (dict): The query to filter the items
            request_key (str): key to lookup currently stored querysets
            use_current (bool): Whether to use current queryset

        Returns:
            QuerySet: The filtered queryset
        """
        if not self.data_model:
            return cast(models.QuerySet, EMPTY_QUERYSET)

        # If provided, use request key to lookup the current (stored) queryset
        if request_key and use_current:
            current = self.get_queryset(request_key, reset=False)
            if current:
                return current

        # Apply optimization: Pre-select related objects
        queryset = self.data_model.objects.all()
        queryset = self._optimize(queryset)

        # Provide the option to specify filter in terms of inclusion/exclusion. Default: Inclusion
        include, exclude = {}, {}
        if query:
            if isinstance(query.get("include"), dict) or isinstance(query.get("exclude"), dict):
                include = query.get("include", {})
                exclude = query.get("exclude", {})
            else:
                include = query

        # Allow to filter using keyword arguments
        filtering_kwargs = {k: v for k, v in kwargs.items()}
        include.update(filtering_kwargs)

        # Apply filters
        queryset = queryset.filter(**include)

        if exclude:
            queryset = queryset.exclude(**exclude)

        queryset = queryset.distinct()

        # Update current version if the request key is provided
        if request_key:
          self.set_queryset(request_key, queryset)

        return queryset


    def update(self, item, query = {}, allow_multiple_updates=False, **kwargs) -> models.QuerySet:
        """
        Updates one or more records in the database

        Args:
            query (dict): The query to find the item to update
            item (dict): The item to update

        Returns:
            Model: The updated model instance
        """
        try:
            query.update(kwargs)
            queryset = self.filter(query)

            if not queryset:
                raise ObjectDoesNotExist

            if len(list(queryset)) > 1 and not allow_multiple_updates:
                raise MultipleObjectsReturned

            for instance in queryset:
                for key, value in item.items():
                    setattr(instance, key, value)
                instance.save()

            self._populate_fields(item)

            return queryset

        except ObjectDoesNotExist as error:
            raise ValueError("The record to update was not found.") from error
        except MultipleObjectsReturned as error:
            raise ValueError("Multiple records matches the query.") from error


    def delete(self, query, allow_multiple_deletions=False, **kwargs):
        """
        Deletes one or more items from the database

        Args:
            query (dict): The query to find the item(s) to delete

        Returns:
          id (int): The id of the record deleted
        """

        try:
            query.update(kwargs)
            queryset = self.filter(query)

            if not queryset:
                raise ObjectDoesNotExist

            if len(list(queryset)) > 1 and not allow_multiple_deletions:
                raise MultipleObjectsReturned

            for item in queryset:
                item.delete()

        except ObjectDoesNotExist as error:
            raise ValueError("The record to delete was not found") from error
        except MultipleObjectsReturned as error:
            raise ValueError("Multiple records matches the query.") from error


    def all(self) -> models.QuerySet:
        """
        Gets all records from the table

        Returns:
            QuerySet: The queryset with all items
        """
        return self.filter()


    def first(self, query={}, by=[], **kwargs):
        """
        Gets the first item from the queryset according to (by) 1 or more fields.

        Returns:
            Instance: The last record by the provided criteria
        """
        if not isinstance(by, list):
            by = list(by)

        filtering_kwargs = {k: v for k, v in kwargs.items() if k in self.field_names}
        query.update(filtering_kwargs)

        instance = self.filter(query).order_by(*by).first()
        if instance:
            self._populate_fields(model_to_dict(instance))

        return instance


    def last(self, query={}, by=[], **kwargs):
        """
        Gets the last item from the queryset according to (by) 1 or more fields.

        Returns:
            Instance: The last record by the provided criteria
        """
        if not isinstance(by, list):
            by = list(by)

        filtering_kwargs = {k: v for k, v in kwargs.items() if k in self.field_names}
        query.update(filtering_kwargs)

        instance = self.filter(query).order_by(*by).last()
        if instance:
            self._populate_fields(model_to_dict(instance))

        return instance

    def none(self):
        """
        Returns an empty queryset.
        """
        return EMPTY_QUERYSET

    ###########################################################################
    #                             PUBLIC METHODS                              #
    ###########################################################################

    def get_related_name(self, neighbour: str) -> str:
        """
        Returns the foreign key facing the neighbour
        """
        return self.foreign_keys.get(neighbour, "")

    def get_queryset(self, request_key: str, reset: bool = True) -> models.QuerySet:
        """
        Returns the queryset corresponding to the hash key. Will first check if
        it exists, otherwise if reset is True, will return a full queryset
        (for all records).
        """
        if not self.data_model:
            return cast(models.QuerySet, EMPTY_QUERYSET)

        if self._querysets.get(request_key, None):
            return self._querysets[request_key]

        if reset:
            self.set_queryset(request_key, reset=True)
            return self._querysets[request_key]

        return self.data_model.objects.none()

    def set_queryset(self, request_key: str, queryset=None, filter_params=None, reset=False) -> None:
        """
        Method to handle specific queryset operations.
        """
        if not self.data_model:
            return

        # overwrite mode
        if queryset:
            self._querysets[request_key] = queryset
            return

        # clear mode
        if reset:
            self._querysets[request_key] = None
            self._querysets[request_key] = self.data_model.objects.all()

        # refine queryset
        if filter_params:
            self._querysets[request_key] = self._querysets[request_key].filter(**filter_params)

    ###########################################################################
    #                            PRIVATE METHODS                              #
    ###########################################################################

    def _initialize(self):
        field_models = {}

        if self.data_model:
            for field in self.data_model._meta.fields:
                if field.name in self.field_names:
                    field_models[field.name] = field

        for field_name in self.field_names:
            field_model = field_models.get(field_name)
            field = TableField(
                name=field_name,
                model=field_model,
                is_related=isinstance(field_model, (models.ForeignKey, models.OneToOneField)),
                is_many_to_many=isinstance(field_model, models.ManyToManyField),
                related_name=getattr(field_model, "related_name", None)
            )
            self.__fields.append(field)

            # Initialize all field attributes as None. Will be set when get() or update()
            setattr(self, field_name, None)

    def _optimize(self, queryset):
        select_related_fields = []
        prefetch_related_fields = []

        for field in self.fields:
            if field.is_related:
                select_related_fields.append(field.name)
            elif field.is_many_to_many:
                prefetch_related_fields.append(field.name)

        if select_related_fields:
            queryset = queryset.select_related(*select_related_fields)
        if prefetch_related_fields:
            queryset = queryset.prefetch_related(*prefetch_related_fields)

        return queryset

    def _populate_fields(self, item: dict):
        for field in self.field_names:
            if field in item:
                setattr(self, field, item[field])

    ###########################################################################
    #                               PROPERTIES                                #
    ###########################################################################

    @property
    def field_names(self) -> list[str]:
        """
        Property to get the field names of the table
        """
        if not self.__field_names:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                  SELECT column_name
                    FROM information_schema.columns
                   WHERE table_name = '{self.db_table_name}'
                   ORDER BY ordinal_position;
                """)
                self.__field_names = [row[0] for row in cursor.fetchall()]

        return self.__field_names

    @property
    def fields(self) -> list[TableField]:
        return self.__fields

    @property
    def data_model(self) -> Optional[Type[models.Model]]:
        return self.__data_model

    @property
    def model_name(self) -> str:
        return self.__model_name

    @model_name.setter
    def model_name(self, name: Optional[str]):
        self.__model_name = name or ""

    @property
    def db_table_name(self) -> str:
        return self.__db_table_name

    @db_table_name.setter
    def db_table_name(self, name: Optional[str]):
        self.__db_table_name = name or ""

    ###########################################################################
    #                               MAGIC METHODS                             #
    ###########################################################################

    def __str__(self):
        return f"{self.table_name} ({self.model_name})"

    def __dict__(self):
        return {name: getattr(self, name) for name in self.field_names}

    def __repr__(self):
        table_details = {
            "name": self.table_name,
            "model": self.model_name,
            "type": self.table_type,
            "dependent": self.dependent_table,
            "fields": self.field_names,
            "neighbours": list(self.neighbours.keys()),
        }

        return json.dumps(table_details)