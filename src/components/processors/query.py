
from typing import Any
from components.processors import Processor
from libs.discovery import load_registered_implementations

class Query(Processor):
    """Handles query operations"""

    queries= {}
    inclusive_operators = {
        'exact': lambda field, value: {f"{field}__exact": value},
        'contains': lambda field, value: {f"{field}__icontains": value},
        'startswith': lambda field, value: {f"{field}__istartswith": value},
        'endswith': lambda field, value: {f"{field}__iendswith": value},
        'below': lambda field, value: {f"{field}__lt": value},
        'over': lambda field, value: {f"{field}__gt": value},
        'in': lambda field, value: {f"{field}__in": value.split(",")},
        'at_least': lambda field, value: {f"{field}__gte": value},
        'at_most': lambda field, value: {f"{field}__lte": value},
        'null': lambda field, value: {f"{field}__isnull": value == 'true'},
    }

    exclusive_operators = {
        'except': lambda field, value: {f"{field}__exact": value},
        'notin': lambda field, value: {f"{field}__in": value.split(",")}
    }

    @staticmethod
    def register_builder(implementation: str):
        """
        Decorator to dynamically register a query class in the `queries` dictionary.
        """
        def decorator(cls):
            Query.queries[implementation] = cls
            return cls
        return decorator

    @staticmethod
    def get_builder(implementation="Default"):
        """SQLQuery factory"""

        if implementation not in Query.queries:
            load_registered_implementations(package_name="components.builders")

        return Query.queries[implementation]

    def fit(self, parameters, request_key = "", backend = "Default", *args, **kwargs) -> dict[str, Any]:
        return Query.get_builder(backend).build(parameters, request_key)