"""
Table Manager class
"""

from abc import abstractmethod
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from components.manager import Manager
from components.preprocessors import PreProcessor
from components.postprocessors import PostProcessor


@Manager.register_manager("Table")
class TableExecutor(Manager):
    """Table Executor abstract class"""

    implementations = {}

    def __init__(self, table):
        self.table = table

    @staticmethod
    def register_implementation(subclass):
        """
        Method that registers the executor class for the specified subclass
        """
        def decorator(cls):
            TableExecutor.implementations[subclass] = cls
            return cls
        return decorator

    @staticmethod
    def get_executor(implementation):
        """
        Executor factory
        """
        if implementation not in TableExecutor.implementations:
            return None

        return TableExecutor.implementations[implementation]

    def execute(self, *args, **kwargs):
        """Method to execute"""
        data = kwargs.get("data", {})
        query = kwargs.get("query", {})
        hash_key = kwargs.get("hash_key", None)
        processor = kwargs.get("processor", None)
        pre_processor = kwargs.get("pre_processor", None)
        post_processor = kwargs.get("post_processor", None)

        # Pre-processing
        pre_processor = pre_processor if pre_processor else processor
        if pre_processor:
            pre_processor = PreProcessor.get_processor(
                implementation=pre_processor, table=self.table
            )
            if pre_processor:
                kwargs["data"] = pre_processor.process(data, hash_key)

        data = self.execute_action(**kwargs)

        if hash_key:
            self.table.set_queryset(hash_key, queryset=data)

        # Post-processing
        post_processor = post_processor if post_processor else processor
        if post_processor:
            post_processor = PostProcessor.get_processor(
                implementation=post_processor, table=self.table
            )
            if post_processor:
                data = post_processor.process(data, hash_key)

        return data

    @abstractmethod
    def execute_action(self, **kwargs):
        """Hook for executing the action"""


###############################################################################
#                                TABLE EXECUTORS                                #
###############################################################################

@TableExecutor.register_implementation("Create")
class CreateTableExecutor(TableExecutor):
    """Table Executor class"""

    def __init__(self, table):
        self.table = table
        super().__init__(table)

    def execute_action(self, data, **kwargs):
        """Method to execute"""
        try:
            if not self.table.data_model:
                raise ValueError(
                    f"Table {self.table.table_name} could not be resolved."
                )

            new_instance = self.table.data_model.objects.create(**data)
            self.table.populate_fields(data)
            data["id"] = new_instance.id

            return data
        except ValueError as error:
            return error


@TableExecutor.register_implementation("Get")
class GetTableExecutor(TableExecutor):
    """Table Executor class to get an item by primary key"""

    def execute_action(self, **kwargs):
        """
        Method to get an item from the table

        Args:
            primary_key (int): The primary key of the item to get

        Returns:
            Model: The model instance
        """
        try:
            primary_key = kwargs.get("primary_key")
            instance = self.table.data_model.objects.get(pk=primary_key)
            self.table.populate_fields(instance.__dict__)
            return instance
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned as error:
            raise ValueError(
                "Multiple objects found with the same primary key."
            ) from error


@TableExecutor.register_implementation("Filter")
class FilterTableExecutor(TableExecutor):
    """Table Executor class to get 1 or more items by means of filtering"""

    def execute_action(self, **kwargs):
        """
        Method to filter items from the table

        Args:
            query (dict): The query to filter the items
            select_related (list): The fields to select related
            prefetch_related (list): The fields to prefetch related

        Returns:
            QuerySet: The filtered queryset
        """
        query = kwargs.get("query", {})
        hash_key = kwargs.get("hash_key", None)
        select_related = kwargs.get("select_related", [])
        prefetch_related = kwargs.get("prefetch_related", [])

        if hash_key:
            queryset = self.table.get_queryset(hash_key, reset=False)
            if queryset:
                return queryset

        formatted_query = {}
        if query and "include" not in query:
            formatted_query["include"] = query
        else:
            formatted_query = query

        queryset = self.table.data_model.objects.all()
        queryset = self.table.optimize_queryset(
            queryset=queryset,
            custom_select_related=select_related,
            custom_prefetch_related=prefetch_related
        )
        items = queryset\
            .filter(**formatted_query.get("include", {}))\
            .exclude(**formatted_query.get("exclude", {}))\
            .distinct()

        return items


@TableExecutor.register_implementation("Update")
class UpdateTableExecutor(TableExecutor):
    """Table Executor class to update an item in the table"""

    def execute_action(self, **kwargs):
        """
        Method to update an item in the table

        Args:
            query (dict): The query to find the item to update
            item (dict): The item to update

        Returns:
            Model: The updated model instance
        """
        query = kwargs.get("query", {})
        item = kwargs.get("item", {})

        try:
            instance = self.table.filter(query)[0]
            for key, value in item.items():
                setattr(instance, key, value)
            instance.save()

            self.table.populate_fields(instance.__dict__)

            return instance
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned as error:
            raise ValueError(
                "Multiple objects found with the same primary key."
            ) from error


@TableExecutor.register_implementation("Delete")
class DeleteTableExecutor(TableExecutor):
    """Table Executor class to delete an item from the table"""

    def execute_action(self, **kwargs):
        """
        Method to delete an item from the table

        Args:
            query (dict): The query to find the item to delete

        Returns:
            bool: True if the item was deleted, False otherwise
        """
        query = kwargs.get("query", {})

        try:
            instance = self.table.filter(query)[0]
            instance.delete()
            return True
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned as error:
            raise ValueError(
                "Multiple objects found with the same primary key."
            ) from error


@TableExecutor.register_implementation("All")
class AllTableExecutor(TableExecutor):
    """Table Executor class to get all items from the table"""

    def execute_action(self, **kwargs):
        """
        Method to get all items from the table

        Returns:
            QuerySet: The queryset with all items
        """
        select_related = kwargs.get("select_related", [])
        prefetch_related = kwargs.get("prefetch_related", [])

        queryset = self.table.data_model.objects.all()
        queryset = self.table.optimize_queryset(
            queryset=queryset,
            custom_select_related=select_related,
            custom_prefetch_related=prefetch_related
        )

        return queryset
