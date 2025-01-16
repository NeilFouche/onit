"""
On It Database Service - Table

Handles table operations

Tables:
    - MySQLTable
"""

import json
from abc import ABC, abstractmethod
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from components.version_control import EntityState
from services.database.tablemanager import TableExecutor


class Table(ABC):
    """ Abstract class (interface)"""

    table_implementations = {}

    def __init__(self, table_name):
        self.table_name = table_name
        self._fields = []

    @staticmethod
    def register_implementation(label):
        """
        Decorator to dynamically register a table class in the `tables` dictionary.
        """
        def decorator(cls):
            Table.table_implementations[label] = cls
            return cls
        return decorator

    @staticmethod
    def get_table(implementation, table_name):
        """Table factory"""

        if implementation not in Table.table_implementations:
            raise ValueError(f"Invalid table type: {implementation}")

        return Table.table_implementations[implementation](table_name)

    @abstractmethod
    def create(self, item, processor="Table:Create", pre_processor=None, post_processor=None):
        """Method to create an item in the table"""

    @abstractmethod
    def get(self, primary_key, processor="Table:Get:SingleRecord", post_processor=None):
        """Method to get an item from the table"""

    @abstractmethod
    def filter(
        self,
        query,
        select_related=None,
        prefetch_related=None,
        processor="Table:Get:MultipleRecords",
        post_processor=None
    ):
        """Method to filter items from the table"""

    @abstractmethod
    def update(
        self,
        query,
        item,
        reason=None,
        processor="Table:Update",
        pre_processor=None,
        post_processor=None
    ):
        """Method to update records"""

    @abstractmethod
    def delete(self, query, processor="Table:Delete", pre_processor=None):
        """Method to delete records"""

    @abstractmethod
    def all(
        self,
        select_related=None,
        prefetch_related=None,
        processor="Table:Get:MultipleRecords",
        post_processor=None
    ):
        """Method to get all records"""

    @abstractmethod
    def _get_fields(self):
        """Method to list the fields of the table"""

    @property
    def field_names(self):
        """
        Property to get the field names of the table
        """
        return []

    @property
    def fields(self):
        """Property to get the fields of the table"""
        return []


###############################################################################
#                            TABLE IMPLEMENTATIONS                            #
###############################################################################

@Table.register_implementation("MySQL")
class MySQLTable(Table):
    """
    Concrete class - MySQL Implementation
    """

    def __init__(self, model):
        self.table_name = model._meta.object_name
        self._data_model = model
        self.id = None
        self.value = None
        self._fields = []
        self._field_names = []
        self._initialize_fields()
        self._type = None
        self._queryset = None
        self._foreign_keys = {}
        self.dependent_table = None

        super().__init__(self.table_name)

    ###########################################################################
    #                             PUBLIC METHODS                              #
    ###########################################################################

    def create(self, item, processor="Table:Create", pre_processor=None, post_processor=None):
        """
        Method to create an item in the table

        Args:
            item (dict): The item to create

        Returns:
            Model: The created model instance
        """
        try:
            executor = TableExecutor.get_executor("Create")(self)
            return executor.execute(
                data=item,
                processor=processor,
                pre_processor=pre_processor,
                post_processor=post_processor
            )
        except ValueError as error:
            return error

    def get(self, primary_key, processor="Table:Get:SingleRecord", post_processor=None):
        """
        Method to get an item from the table

        Args:
            primary_key (int): The primary key of the item to get

        Returns:
            Model: The model instance
        """
        try:
            executor = TableExecutor.get_executor("Get")(self)
            return executor.execute(
                primary_key=primary_key,
                processor=processor,
                post_processor=post_processor
            )
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned as error:
            raise ValueError(
                "Multiple objects found with the same primary key."
            ) from error

    def filter(
        self,
        query,
        select_related=None,
        prefetch_related=None,
        processor="Table:Get:MultipleRecords",
        post_processor=None
    ):
        """
        Method to filter items from the table

        Args:
            query (dict): The query to filter the items
            select_related (list): The fields to select related
            prefetch_related (list): The fields to prefetch related

        Returns:
            QuerySet: The filtered queryset
        """
        executor = TableExecutor.get_executor("Filter")(self)
        return executor.execute(
            query=query,
            select_related=select_related,
            prefetch_related=prefetch_related,
            processor=processor,
            post_processor=post_processor
        )

    def update(
        self,
        query,
        item,
        reason=None,
        processor="Table:Update",
        pre_processor=None,
        post_processor=None
    ):
        """
        Method to update an item in the table

        Args:
            query (dict): The query to find the item to update
            item (dict): The item to update

        Returns:
            Model: The updated model instance
        """
        try:
            executor = TableExecutor.get_executor("Update")(self)
            return executor.execute(
                query=query,
                item=item,
                reason=reason,
                processor=processor,
                pre_processor=pre_processor,
                post_processor=post_processor
            )
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned as error:
            raise ValueError(
                "Multiple objects found with the same primary key."
            ) from error

    def delete(self, query, processor="Table:Delete", pre_processor=None):
        """
        Method to delete an item from the table

        Args:
            query (dict): The query to find the item to delete

        Returns:
            bool: True if the item was deleted, False otherwise
        """
        try:
            executor = TableExecutor.get_executor("Delete")(self)
            return executor.execute(
                query=query,
                processor=processor,
                pre_processor=pre_processor
            )
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned as error:
            raise ValueError(
                "Multiple objects found with the same primary key."
            ) from error

    def all(
        self,
        select_related=None,
        prefetch_related=None,
        processor="Table:Get:MultipleRecords",
        post_processor=None
    ):
        """
        Method to get all items from the table
        """
        executor = TableExecutor.get_executor("All")(self)
        return executor.execute(
            select_related=select_related,
            prefetch_related=prefetch_related,
            processor=processor,
            post_processor=post_processor
        )

    def create_state(self, context="General"):
        """
        Method to create a memento

        Args:
            item (dict): A query to find the item to save

        Returns:
            EntityState: The state of the item
        """

        return EntityState(
            table=self.table_name,
            entity={
                "entity_id": self.id,
                "entity_key": f"Table:{self.table_name}:{context}",
                "value": self.value
            })

    def restore(self, state):
        """
        Method to restore a memento

        Args:
            state (EntityState): The state to restore
        """
        model = self._data_model
        instance = model.objects.get(pk=state.entity_id)
        instance.value = state[state.value]
        instance.save()

    def optimize_queryset(
        self,
        queryset,
        custom_select_related=None,
        custom_prefetch_related=None
    ):
        """
        Method to optimize the queryset

        Args:
            queryset (QuerySet): The queryset to optimize.
            query (dict): The query to filter the queryset.
            custom_select_related (list): The custom select related fields.
            custom_prefetch_related (list): The custom prefetch related fields.

        Returns:
            QuerySet: The optimized queryset.
        """
        select_related_fields = custom_select_related or []
        prefetch_related_fields = custom_prefetch_related or []

        # Identify fields related to relationships
        if not custom_select_related or not custom_prefetch_related:
            for field in self.fields:
                if not custom_select_related and self._is_foreign_key(field):
                    select_related_fields.append(field.name)
                elif not custom_prefetch_related and self._is_many_to_many(field):
                    prefetch_related_fields.append(field.name)

        # Apply optimizations
        if select_related_fields:
            queryset = queryset.select_related(*select_related_fields)
        if prefetch_related_fields:
            queryset = queryset.prefetch_related(*prefetch_related_fields)

        return queryset

    def populate_fields(self, item):
        """
        Method to update the fields of the table

        Args:
            item (dict): The item to update the fields with
        """
        for field in self.field_names:
            if field in item:
                setattr(self, field, item[field])

    def get_related_name(self, neighbour):
        """
        Returns the foreign key facing the neighbour
        """
        return self._foreign_keys.get(neighbour)

    ###########################################################################
    #                            PRIVATE METHODS                              #
    ###########################################################################

    def _get_fields(self):
        """
        Method to list the fields of the table

        Returns:
            list: The fields of the table
        """
        return self._data_model._meta.get_fields()

    def _initialize_fields(self):
        """
        Method to initialize the fields of the table
        """
        if not self._fields:
            self._fields = self._get_fields()

        for field in self._fields:
            setattr(self, f"_{field.name}", field)

    def _is_foreign_key(self, field):
        """
        Method to check if the field is a foreign key

        Args:
            field (Field): The field to check

        Returns:
            bool: True if the field is a foreign key, False otherwise
        """
        return isinstance(field, (models.ForeignKey, models.OneToOneField))

    def _is_many_to_many(self, field):
        """
        Method to check if the field is a many to many

        Args:
            field (Field): The field to check

        Returns:
            bool: True if the field is a many to many, False otherwise
        """
        return isinstance(field, models.ManyToManyField)

    ###########################################################################
    #                          PROPERTIES & SETTERS                           #
    ###########################################################################

    @property
    def field_names(self):
        """
        Property to get the field names of the table
        """
        return [field.name for field in self.fields]

    @property
    def fields(self):
        """
        Property to get the fields of the table

        Returns:
            list: The fields of the table
        """
        if not self._fields:
            self._fields = self._get_fields()
        return self._fields

    @property
    def model_name(self):
        """
        Property to get the model name

        Returns:
            str: The model name
        """
        return self._data_model._meta.object_name

    @property
    def data_model(self):
        """
        Property to get the model

        Returns:
            Model: The model
        """
        return self._data_model

    @property
    def is_intermediate(self):
        """
        Property to get the type of the table

        Returns:
            str: The type of the table
        """
        return self._type and self._type == "intermediate"

    @property
    def queryset(self):
        """
        Returns the queryset saved with last fetch.

        If none, returns the queryset for all records
        """
        if not self._queryset:
            self._queryset = self._data_model.objects.all()

        return self._queryset

    @queryset.setter
    def queryset(self, queryset):
        """
        Setter for the queryset
        """
        self._queryset = queryset

    @property
    def foreign_keys(self):
        """
        Returns the foreign keys of the table
        """
        return self._foreign_keys

    @foreign_keys.setter
    def foreign_keys(self, foreign_keys):
        """
        Setter for the foreign keys related to the respective neighbours
        """
        self._foreign_keys = foreign_keys

    @property
    def type(self):
        """
        Returns the type of the table
        """
        return self._type

    @type.setter
    def type(self, table_type):
        """
        Setter for the table type
        """
        self._type = table_type

    ###########################################################################
    #                               MAGIC METHODS                             #
    ###########################################################################

    def __str__(self):
        return self.table_name

    def __repr__(self):
        table_details = {
            "name": self.table_name,
            "type": self.type,
            "dependent": self.dependent_table,
            "fields": self.field_names
        }
        return json.dumps(table_details)
        # return self.table_name
