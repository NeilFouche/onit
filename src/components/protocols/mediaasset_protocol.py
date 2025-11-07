from typing import Protocol, Any, Type
from django.db import models
from api.models import EntityMedia
from datetime import date

from components.dataclasses import TableField

class MediaAssetTable(Protocol):
    table_name: str
    id: int
    key: str
    content_type_id: int
    dependent_table: str
    foreign_keys: dict[str, str]
    neighbours: list[dict[str, Any]]
    table_type: str
    weight: int

    mediaentities: EntityMedia
    id: int
    key: str
    label: str
    slug: str
    description: str
    credit: str
    format: str
    relative_path: str
    filesize: int
    timestamp: float
    width: int
    height: int
    created_date: date
    category: str

    def all(self) -> models.QuerySet:
        '''Gets all records from the table'''
        ...

    def create(self, item: dict) -> int:
        '''Creates an record in the database'''
        ...

    def delete(self, query, allow_multiple_deletions=False, **kwargs):
        '''Deletes one or more items from the database'''

    def filter(self, query = {}, request_key = None, use_current = True, **kwargs) -> models.QuerySet:
        '''Gets multiple records from the database.'''
        ...

    def first(self, query={}, by=[], **kwargs) -> models.Model:
        ''' Gets the first item from the queryset according to (by) 1 or more fields.'''
        ...

    def last(self, query={}, by=[], **kwargs) -> models.Model:
        '''Gets the last item from the queryset according to (by) 1 or more fields.'''
        ...

    def get(self, *args, **kwargs) -> models.Model:
        '''Gets a record from the database'''
        ...

    def get_related_name(self, neighbour: str) -> str | None:
        '''Returns the foreign key facing the neighbour.'''
        ...

    def get_queryset(self, request_key, reset=True) -> models.QuerySet | None:
        '''Returns the queryset corresponding to the hash key. Will first check if it exists, otherwise if reset is True, will return a full queryset (for all records)'''
        ...

    def set_queryset(self, request_key, queryset=None, filter_params=None, reset=False) -> None:
        '''Method to handle specific queryset operations'''

    def update(self, item, query = {}, allow_multiple_updates=False, **kwargs) -> models.QuerySet:
        '''Updates one or more records in the database'''
        ...

    @property
    def field_names(self) -> list[str]: ...

    @property
    def fields(self) -> TableField: ...

    @property
    def data_model(self) -> Type[models.Model]: ...

    @property
    def model_name(self) -> str: ...
