"""
On It Database Service - Query

Handles query operations

Queries:
    - MySQLQuery
"""


class Query():
    """Handles query operations"""

    query_implementations = {}
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
    def register_implementation(label):
        """
        Decorator to dynamically register a query class in the `queries` dictionary.
        """
        def decorator(cls):
            Query.query_implementations[label] = cls
            return cls
        return decorator

    @staticmethod
    def get_query(implementation="Django"):
        """Query factory"""

        if implementation not in Query.query_implementations:
            raise ValueError(f"Invalid query type: {implementation}")

        return Query.query_implementations[implementation]

    @staticmethod
    def build(query_parameters, backend="Django"):
        """Method to build a query"""
        return Query.get_query(backend).build(query_parameters)


###############################################################################
#                            QUERY IMPLEMENTATIONS                            #
###############################################################################

@Query.register_implementation('Django')
class DjangoQuery():
    """ Django Query """

    @staticmethod
    def build(query_parameters):
        """Method to build a query"""
        filter_params = {}
        include_params = {}
        exclude_params = {}

        if not query_parameters:
            return filter_params

        for key, value in query_parameters.items():
            if key == 'table':
                continue

            if ":" in value:
                operation, raw_value = value.split(":", 1)
                if operation in Query.inclusive_operators:
                    field_query = Query.inclusive_operators[operation](
                        key, raw_value
                    )
                    include_params.update(field_query)
                elif operation in Query.exclusive_operators:
                    field_query = Query.exclusive_operators[operation](
                        key, raw_value
                    )
                    exclude_params.update(field_query)
            else:
                include_params[key] = value if value != 'true' else True

        filter_params["include"] = include_params
        filter_params["exclude"] = exclude_params

        return filter_params
