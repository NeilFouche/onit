import os
import sys
import django
from pathlib import Path
from django.apps import apps
from django.db import models

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from libs.strings import camel_to_snake

def table_protocols():
    for model in apps.get_models():
        model_name = model.__name__

        protocol_file_path = Path(f"components/protocols/{model_name.lower()}_protocol.py")
        with protocol_file_path.open("w") as file:
            # Imports
            related_models = get_related_models(model)
            date_related_imports = get_date_related_imports(model)

            file.write("from typing import Protocol, Any, Type\n")
            file.write("from django.db import models\n")
            if related_models:
                import_lines = get_import_lines(related_models)
                for line in import_lines:
                    file.write(f"{line}\n")
            if date_related_imports:
                file.write(f"from datetime import {', '.join(date_related_imports)}\n")

            file.write("\n")
            file.write("from components.dataclasses import TableField\n")

            # Protocol class
            file.write("\n")
            file.write(f"class {model_name}Table(Protocol):\n")

            # Fields
            file.write("    table_name: str\n")
            file.write("    id: int\n")
            file.write("    key: str\n")
            file.write("    content_type_id: int\n")
            file.write("    dependent_table: str\n")
            file.write("    foreign_keys: dict[str, str]\n")
            file.write("    neighbours: list[dict[str, Any]]\n")
            file.write("    table_type: str\n")
            file.write("    weight: int\n\n")

            for field in model._meta.get_fields():
                if hasattr(field, "name"):
                    field_type = get_datatype(field)
                    file.write(f"    {field.name}: {field_type}\n")

            # Methods
            file.write("\n")
            file.write("    def all(self) -> models.QuerySet:\n        '''Gets all records from the table'''\n        ...\n\n")
            file.write("    def create(self, item: dict) -> int:\n        '''Creates an record in the database'''\n        ...\n\n")
            file.write("    def delete(self, query, allow_multiple_deletions=False, **kwargs):\n        '''Deletes one or more items from the database'''\n\n")
            file.write("    def filter(self, query = {}, request_key = None, use_current = True, **kwargs) -> models.QuerySet:\n        '''Gets multiple records from the database.'''\n        ...\n\n")
            file.write("    def first(self, query={}, by=[], **kwargs) -> models.Model:\n        ''' Gets the first item from the queryset according to (by) 1 or more fields.'''\n        ...\n\n")
            file.write("    def last(self, query={}, by=[], **kwargs) -> models.Model:\n        '''Gets the last item from the queryset according to (by) 1 or more fields.'''\n        ...\n\n")
            file.write("    def get(self, *args, **kwargs) -> models.Model:\n        '''Gets a record from the database'''\n        ...\n\n")
            file.write("    def get_related_name(self, neighbour: str) -> str | None:\n        '''Returns the foreign key facing the neighbour.'''\n        ...\n\n")
            file.write("    def get_queryset(self, request_key, reset=True) -> models.QuerySet | None:\n        '''Returns the queryset corresponding to the hash key. Will first check if it exists, otherwise if reset is True, will return a full queryset (for all records)'''\n        ...\n\n")
            file.write("    def set_queryset(self, request_key, queryset=None, filter_params=None, reset=False) -> None:\n        '''Method to handle specific queryset operations'''\n\n")
            file.write("    def update(self, item, query = {}, allow_multiple_updates=False, **kwargs) -> models.QuerySet:\n        '''Updates one or more records in the database'''\n        ...\n\n")

            # Properties
            file.write("    @property\n")
            file.write("    def field_names(self) -> list[str]: ...\n\n")
            file.write("    @property\n")
            file.write("    def fields(self) -> TableField: ...\n\n")
            file.write("    @property\n")
            file.write("    def data_model(self) -> Type[models.Model]: ...\n\n")
            file.write("    @property\n")
            file.write("    def model_name(self) -> str: ...\n")

def database_protocol():
    db_protocol_path = Path("components/protocols/database_protocol.py")

    with db_protocol_path.open('w') as file:
        # Imports
        file.write("from typing import Protocol, Optional\n")
        file.write(f"from django.db.models import QuerySet\n")
        file.write("from components.graphs.graph import Graph\n")
        file.write("from components.sources.databases import Table\n\n")

        for model in apps.get_models():
            model_name = model.__name__
            file.write(f"from components.protocols.{model_name.lower()}_protocol import {model_name}Table\n")

        # Class
        file.write("\n")
        file.write(f"class RelationalDatabase(Protocol):\n")

        # Fields
        for model in apps.get_models():
            model_name = model.__name__
            file.write(f"    {camel_to_snake(model_name)}: {model_name}Table\n")

        # Methods
        file.write("\n")
        file.write("    def get(self, table_name: Optional[str] = None, model_name: Optional[str] = None, content_type_id: Optional[int] = None) -> Table: ...\n")

        # Properties
        file.write("\n")
        file.write("    @property\n")
        file.write("    def table_names(self) -> list[str]: ...\n\n")
        file.write("    @property\n")
        file.write("    def name(self) -> str: ...\n\n")
        file.write("    @property\n")
        file.write("    def schema(self) -> dict: ...\n\n")
        file.write("    @property\n")
        file.write("    def schema_graph(self) -> Graph: ...\n")

def get_related_models(model):
    return [
        (field.related_model.__name__, field.related_model._meta.app_label)
        for field in model._meta.get_fields()
        if isinstance(field, (models.ForeignKey, models.ManyToManyRel, models.ManyToOneRel, models.OneToOneRel, models.ManyToManyField))
    ]

def get_datatype(field):
    related_key = field.related_model.__name__ if hasattr(field, 'related_model') and field.related_model is not None else "FK"
    types = {
        "str": (models.CharField, models.TextField),
        "int": models.IntegerField,
        "float": models.FloatField,
        "bool": models.BooleanField,
        "date": models.DateField,
        "time": models.TimeField,
        "datetime": models.DateTimeField,
        related_key: (
            models.ForeignKey,
            models.ManyToManyRel,
            models.ManyToManyField,
            models.ManyToOneRel,
            models.OneToOneRel
        )
    }

    for data_type, field_types in types.items():
        if isinstance(field, field_types):
            return data_type

    return "Any"

def get_date_related_imports(model):
    imports = []
    for field in model._meta.get_fields():
        if isinstance(field, models.DateField):
            imports.append("date")
        if isinstance(field, models.TimeField):
            imports.append("time")
        if isinstance(field, models.DateTimeField):
            imports.append("datetime")

    return imports

def get_import_lines(related_models):
    apps = {}

    for rel_model, app in related_models:
        if app not in apps:
            apps[app] = []
        apps[app].append(rel_model)

    return [
        f"from {'django.contrib.' if app != 'api' else ''}{app}.models import {', '.join(items)}"
        for app, items in apps.items()
    ]


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onit.settings")
    django.setup()

    table_protocols()
    database_protocol()