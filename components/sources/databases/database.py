
import json
from pathlib import Path
from typing import Optional, Set, Type

from django.apps import apps
from django.db import connection
from django.db.models import ManyToManyField, Model
from django.contrib.contenttypes.models import ContentType

from components.graphs import Graph
from components.sources.databases import Database, Table
from libs.strings import camel_to_snake
from services.database import DatabaseService

@DatabaseService.register_database("PostgreSQL")
class PostgreSQLDatabase(Database):

    def __init__(self) -> None:
        self.engine = "PostgreSQL"
        self.__name = ""
        self.__schema = {}
        self.__schema_graph = None
        self.__table_names = []
        self.__data_models = set()
        self._model_name_by_db_table_name: dict[str, str] = {}
        self._db_table_name_map: dict[str, str] = {}
        self._db_table_names: dict[str, str] = {}
        self._models: dict[str, Type[Model]] = {}
        self._model_name_map: dict[str, str] = {}
        self._model_names: dict[str, str] = {}
        self._content_types_map: dict[int, str] = {}
        self._content_types: dict[str, int] = {}

        self._initialize()

    def get(
        self,
        table_name: Optional[str] = None,
        model_name: Optional[str] = None,
        content_type_id: Optional[int] = None,
        db_table_name: Optional[str] = None
    ) -> Table:
        provided_field = "table name"
        provided_value = None

        if content_type_id:
            provided_field = "content type id"
            provided_value = content_type_id
            table_name = self._content_types_map.get(content_type_id)

        if model_name:
            provided_field = "model name"
            provided_value = model_name
            table_name = self._model_name_map.get(model_name)

        if db_table_name:
            provided_field = "db table name"
            provided_value = db_table_name
            table_name = self._db_table_name_map.get(db_table_name)

        if table_name is None:
            raise ValueError(f"Table with {provided_field} = {provided_value} is unknown.")

        return getattr(self, table_name)

    def _get_content_type_id(self, model_name: str) -> int:
        content_type = ContentType.objects.get(app_label="api", model=model_name)
        return content_type.pk

    def get_models(self) -> Set[Type[Model]]:
        all_models: Set[Type[Model]] = set(apps.get_models())

        for model in all_models.copy():
            for field in model._meta.get_fields():
                if isinstance(field, ManyToManyField):
                    through_model = field.remote_field.through  # type: ignore
                    if through_model:
                        all_models.add(through_model)

        return all_models

    def map_table_models(self):
        for model in self.data_models:
            db_table_name = model._meta.db_table
            model_name = model._meta.object_name or ""
            self._model_name_by_db_table_name[db_table_name] = model_name

            table_name = camel_to_snake(model_name)
            self._db_table_name_map[db_table_name] = table_name
            self._db_table_names[table_name] = db_table_name

            self._models[table_name] = model
            self._model_name_map[model_name] = table_name
            self._model_names[table_name] = model_name

            app_label = model._meta.app_label
            content_type_label = model_name.replace("_", "").lower()
            content_type = ContentType.objects.filter(app_label=app_label, model=content_type_label).first()
            if content_type:
                self._content_types_map[content_type.pk] = table_name
                self._content_types[table_name] = content_type.pk

    def _initialize(self):
        self.map_table_models()
        schema = self.schema
        for table_name in self.table_names:
              table = Table(
                  table_name=table_name,
                  db_table_name=self._db_table_names.get(table_name),
                  model=self._models.get(table_name)
              )
              table.model_name = self._model_names.get(table_name)
              table.content_type_id = self._content_types.get(table_name, 0)

              table_schema = schema.get(table.model_name)
              if table_schema:
                  table.dependent_table = table_schema.get("dependent_table", None)
                  table.foreign_keys = table_schema.get("foreign_keys", {})
                  table.neighbours = table_schema.get("neighbours", {})
                  table.table_type = table_schema.get("type", None)
                  table.weight = table_schema.get("weight", 1)

              setattr(self, table_name, table)

    ###########################################################################
    #                               PROPERTIES                                #
    ###########################################################################

    @property
    def table_names(self) -> list[str]:
        if not self.__table_names:
            with connection.cursor() as cursor:
                cursor.execute("""
                  SELECT tablename
                    FROM pg_catalog.pg_tables
                   WHERE schemaname = 'public'
                """)

                db_table_names  = [row[0] for row in cursor.fetchall()]

            self.__table_names = list({
                self._db_table_name_map[name]
                for name in db_table_names
                if name in self._db_table_name_map
            })

        return self.__table_names

    @property
    def name(self) -> str:
        if self.__name == "":
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database();")
                data = cursor.fetchone()
                if data:
                  self.__name = data[0]
        return self.__name

    @property
    def data_models(self) -> Set[Type[Model]]:
        if not self.__data_models:
            self.__data_models = self.get_models()
        return self.__data_models

    @property
    def schema(self) -> dict:
        if not self.__schema:
            schema_path = Path("data/database_specifications/database_schema.json")
            with open(schema_path, 'r') as file:
                self.__schema = json.load(file)

        return self.__schema

    @property
    def schema_graph(self) -> Graph:
        if self.__schema_graph is None:
            graph = Graph()

            for table_name, value in self.schema.items():
                graph.add_node(table_name, value)

            self.__schema_graph = graph

        self.__schema_graph.reset()

        return self.__schema_graph

