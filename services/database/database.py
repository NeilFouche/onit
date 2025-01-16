"""
On It Database Service - Database

Handles database operations

Databases:
    - MySQLDatabase
"""

import json
from django.apps import apps
from django.core.cache import caches
from django.db.models import QuerySet
from django.db import connection
from libs.algorithms import a_star
from libs.strings import camel_to_snake
from components import SchemaGraph
from components.postprocessors import PostProcessor
from services.database import Query, QueryPath, Table
from services.transformer import TransformerService


class DatabaseService():
    """Singleton class to handle database operations"""

    _instance = None
    _default_cache = caches["default"]

    ###########################################################################
    #                        SINGLETON INITIALIZATION                         #
    ###########################################################################

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            database_name = kwargs.get("database", "MySQL")
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance._initialize_instance(database_name)
        return cls._instance

    def __init__(self, database):
        self.database_name = database
        self._schema = None
        self.tables = None
        self._table_names = None
        self._initialized = False

        if not hasattr(self, "_intermediate_tables"):
            self._intermediate_tables = []

        if not hasattr(self, "_table_types"):
            self._table_types = {}

    def _initialize_instance(self, database_name):
        """Method to initialize the instance"""
        if not hasattr(self, "_initialized"):
            self.database_name = database_name
            self.tables = self._get_tables()
            self._schema = self._get_schema()
            self._initialized = True

    ###########################################################################
    #                             STATIC METHODS                              #
    ###########################################################################

    @staticmethod
    def get_database(app="front"):
        """
        Method to get the database
        """
        return apps.get_app_config(app).database

    ###########################################################################
    #                             PUBLIC METHODS                              #
    ###########################################################################

    def fetch_data(self, target, filter_params, source=None):
        """
        Method to fetch data from the database
        """
        source = self._verify_source(
            source=source, filter=filter_params, default=target
        )

        source_table = self.get_table(camel_to_snake(source))
        query = Query.build(filter_params)
        queryset = source_table.filter(query, processor=None)

        if source != target:
            path = self.get_query_path(source, target)
            im_nodes = self._identify_intermediate_nodes(path)

            for i in range(len(im_nodes) - 1):
                next_im = im_nodes[i+1]
                next_segment = self._get_segment(
                    path=path, next_im=next_im, current_location=im_nodes[i]
                )

                # Reduce path if necessary
                if len(next_segment) > 1:
                    filter_params = {
                        "id__in": queryset.values_list("id", flat=True)
                    }
                    queryset = self._reduce_segment(
                        next_segment, filter_params)

                # Break if there are no more intermediate nodes
                if next_im == len(path):
                    break

                predecessor = self.get_table(path.names[next_im+1])
                predecessor.queryset = queryset
                queryset = self.resolve_intermediate_relationship(
                    predecessor=predecessor,
                    intermediate_table=self.get_table(path.names[next_im]),
                    successor=self.get_table(path.names[next_im-1])
                )

        post_processor = PostProcessor.get_processor(
            implementation="Table:Get:MultipleRecords",
            table=self.get_table(camel_to_snake(target))
        )

        return post_processor.process(queryset)

    def _reduce_segment(self, query_path, query_parameters):
        """
        Method to fetch data from the database
        """
        if not query_path:
            return []

        # Build query_key_string from query_path
        query_key = [
            data["foreign_key"] for data in query_path if data["foreign_key"]
        ]
        query_key_string = "__".join(query_key)

        filtered_params = {}
        query = Query.build(query_parameters)
        for params_type, params in query.items():
            filtered_params[params_type] = {}
            for key in params.keys():
                filtered_params[params_type][f"{query_key_string}__{key}"] = params[key]

        # Fetch the data
        end_table_data = query_path.first
        end_table_name = end_table_data["table_name"]
        end_table = self.get_table(camel_to_snake(end_table_name))

        return end_table.filter(filtered_params, processor=None)

    def resolve_intermediate_relationship(
        self, predecessor: Table, intermediate_table: Table, successor: Table
    ) -> QuerySet:
        """
        Method to resolve the intermediate relationship

        :param predecessor: The predecessor
        :param intermediate_table: The intermediate table
        :param successor: The successor
        :return: The queryset
        """

        if self._approaching_from_left(predecessor, intermediate_table):
            return self._resolve_from_left(predecessor, intermediate_table, successor)

        return self._resolve_from_right(predecessor, intermediate_table, successor)

    def get_query_path(self, start_table, end_table):
        """
        Retrieves the path from the cache if it exists, otherwise computes the shortest path
        between the two tables and caches it.
        """
        path = DatabaseService._default_cache.get(
            f"QueryPath:{start_table}:{end_table}"
        )

        if not path:
            # Calculate the shortest path between the two tables
            schema_graph = self._schema
            if not schema_graph:
                schema_graph = self._get_schema()
            path = a_star(schema_graph, start_table, end_table)
            DatabaseService._default_cache.set(
                f"QueryPath:{start_table}:{end_table}", json.dumps(path)
            )

        if isinstance(path, str):
            path = json.loads(path)

        return QueryPath(path)

    def get_table(self, table_name: str):
        """Method to get a table by name"""
        return getattr(self, table_name)

    ###########################################################################
    #                             PRIVATE METHODS                             #
    ###########################################################################

    def _approaching_from_left(self, predecessor: Table, intermediate_table: Table) -> bool:
        """
        Approach the intermediate table from the left,
        i.e. querying all related records for an owning entity.

        Example:
        Approaching from left: Media -> EntityMedia -> Entity
        * Get all entities associated with a particular media record.

        Approaching from right: Media <- EntityMedia <- Entity
        * Get all media associated with a particular entity record.

        :param predecessor: The owning table, e.g. Media
        :param intermediate_table: The intermediate table, e.g. EntityMedia
        :return: True if approaching from the left, False otherwise
        """

        return predecessor.table_name == intermediate_table.dependent_table

    def _get_segment(self, path, next_im, current_location):
        """
        Returns all the nodes between current location and the next intermediate node
        """
        return QueryPath(path[current_location+1:next_im])

    def _get_schema(self):
        """
        Method to get the schema for the database
        """
        parameters = self.get_table("parameter")
        db_schema_parameter = parameters.\
            filter({"key": "Database:Schema:Global"})

        db_schema = db_schema_parameter[0].get("value", None)

        schema = SchemaGraph()
        for table_name, table_schema in db_schema.items():
            # Create nodes for the current table on the graph
            schema.add_node(table_name, table_schema)

            # Update table configuration
            table_attribute_name = camel_to_snake(table_name)
            if not hasattr(self, table_attribute_name):
                continue

            table = self.get_table(table_attribute_name)
            table_type = table_schema.get("type", None)
            table.type = table_type
            table.dependent_table = table_schema.get("dependent_table", None)
            table.foreign_keys = table_schema["foreign_keys"]

            if not hasattr(self, "_intermediate_tables"):
                setattr(self, "_intermediate_tables", [])
            if table_type == "intermediate":
                self._intermediate_tables.append(table_name)

            # Update table types dictionary
            if not hasattr(self, "_table_types"):
                setattr(self, "_table_types", {})
            self._table_types[table_name] = table_type

        return schema

    def _get_tables(self):
        """
        Checks all of the tables in the database and creates an attribute for each.
        The table can then accessed like:

        Uses:
            * product_table = proddb.product
            * product_records = proddb.product.get(query)
            * table = database.get_table(table_name)
        """
        tables = []

        for table_name in self.table_names:
            model = self._get_model(table_name)
            if model:
                table = Table.get_table(self.database_name, model)
                tables.append(table)
                setattr(
                    self, camel_to_snake(model._meta.object_name), table
                )

        return tables

    def _get_model(self, table_name):
        """
        Method to check if the table has a model
        """
        for model in apps.get_models():
            if model._meta.db_table == table_name:
                return model

        return None

    def _verify_source(self, source, filter, default):
        """
        Method to get the source
        """
        if source:
            return source

        source = filter.get("table", None)

        return source if source else default

    def _identify_intermediate_nodes(self, path):
        """
        Method to identify the intermediate nodes in the path

        Args:
            path (QueryPath): The path to identify the intermediate nodes

        Returns:
            list: The list of intermediate nodes
        """
        intermediate_nodes = [
            i for i, node in enumerate(path) if node["table_name"] in self._intermediate_tables
        ]

        return [-1] + intermediate_nodes + [len(path)]

    def _resolve_from_left(self, predecessor, intermediate_table, successor):
        """
        Method to resolve the query from the left
        """
        intermediate_related_name = intermediate_table.get_related_name(
            neighbour=predecessor.table_name
        )
        filter_params = {
            "content_type__model": successor.model_name,
            f"{intermediate_related_name}__in": predecessor.queryset.values_list("id", flat=True)
        }
        intermediate_values = intermediate_table.queryset.\
            filter(**filter_params).\
            values_list("object_id", flat=True)

        return successor.queryset.filter(id__in=intermediate_values)

    def _resolve_from_right(self, predecessor, intermediate_table, successor):
        """
        Method to resolve the query from the right
        """
        left_related_name = successor.get_related_name(
            neighbour=intermediate_table.table_name
        )
        intermediate_values = predecessor.queryset.values_list("id", flat=True)
        filter_parameters = {
            f"{left_related_name}__content_type__model": predecessor.model_name,
            f"{left_related_name}__object_id__in": intermediate_values
        }

        return successor.queryset.filter(**filter_parameters)

    ###########################################################################
    #                               PROPERTIES                                #
    ###########################################################################

    @property
    def table_names(self):
        """Property to get the table names"""
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            return [table[0] for table in cursor.fetchall()]

    ###########################################################################
    #                             SPECIAL METHODS                             #
    ###########################################################################

    def __str__(self):
        return f"{self.database_name} Database"
