from components.processors.query import Query
from services.rest import RestService

@Query.register_builder('Default')
class QueryBuilder():
    """Default query builder"""

    @staticmethod
    def fit(query_parameters, *args, **kwargs):
        """A method for building queries that handles exact and ranged criteria"""
        filter_params = {}
        include_params = {}
        exclude_params = {}

        if not query_parameters:
            return filter_params

        for key, value in query_parameters.items():

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