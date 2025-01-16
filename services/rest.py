"""
On It REST Service

Handles REST API requests
"""

import json
import hashlib
import sys
from django.http import JsonResponse
from django.middleware.csrf import get_token
from libs.strings import camel_to_snake, kebab_to_camel


class RestService():
    """Handles REST API requests"""

    request = None
    views = {}

    @staticmethod
    def error_response(error, status=400):
        """Method to return an error response"""
        return JsonResponse({
            'success': False,
            'message': error,
        }, status=status)

    @staticmethod
    def get_token(request):
        """Method to get the CSRF token"""
        return JsonResponse({'csrf_token': get_token(request)})

    @staticmethod
    def get_endpoint():
        """Method to get the endpoint"""
        path = RestService.request.path.rstrip('/')
        path_parts = path.split('/')
        return path_parts[2]

    @staticmethod
    def get_context():
        """Method to get context if provided"""
        path = RestService.request.path.rstrip('/')
        path_parts = path.split('/')
        return path_parts[-1] if len(path_parts) > 2 else None

    @staticmethod
    def get_hash():
        """
        Method to get the hash

        The hash is generated based on the target table, starting table,
        and query parameters.

        Returns:
            str: The hashed key.
        """
        target_table = RestService.get_target_table()
        parts = [
            target_table,
            RestService.get_starting_table() or target_table,
            json.dumps(RestService.get_query_parmeters())
        ]
        raw_key = ':'.join(parts)
        hash_object = hashlib.md5(raw_key.encode('utf-8'))

        return hash_object.hexdigest()

    @staticmethod
    def get_message(data, table_name):
        """Method to get the message"""
        return "No records found" if not data else f"{table_name} records retrieved succesfully"

    @staticmethod
    def get_query_parmeters():
        """Method to get the query parameters"""
        return {
            key: value
            for key, value in RestService.request.GET.items() if key != 'table'
        }

    @staticmethod
    def get_request_body():
        """Method to get the request body"""
        return RestService.request.body.decode('utf-8')

    @staticmethod
    def get_starting_table():
        """Method to get the starting table"""
        return RestService._get_table_parameter()

    @staticmethod
    def get_target_table():
        """Method to get the target table"""
        return kebab_to_camel(RestService.get_endpoint())

    @staticmethod
    def get_table_name():
        """
        Method to get the table name

        Note: If the table name is not provided as a query parameter, use the endpoint.

        Returns:
            str: The table name converted to snake_case.
        """
        table_name = RestService._get_table_parameter()
        if not table_name:
            table_name = RestService.get_endpoint()

        return camel_to_snake(table_name)

    @staticmethod
    def get_view():
        """Method to get the view"""
        if RestService._is_token_endpoint():
            return RestService.views['get_token']

        return RestService.views[RestService.request.method]

    @staticmethod
    def register_view(label):
        """
        Decorator to dynamically register a view function in the `views` dictionary.
        """
        def decorator(cls):
            RestService.views[label] = cls
            return cls
        return decorator

    @staticmethod
    def response(data, error=None):
        """Method to return a response"""
        try:
            # Raise the error if it was triggered by previous processes, e.g. validation
            if error:
                raise ValueError(error)

            table = RestService.get_table_name()
            message = RestService.get_message(data, table.title())
            entities = RestService.get_query_parmeters()

            return JsonResponse({
                "message": message,
                "status": 200,
                "table": table,
                "results": len(data) if data else 0,
                "size (bytes)": sys.getsizeof(data),
                "query parameters": entities,
                "data": data
            })
        except ValueError as e:
            return JsonResponse({
                "status": 400,
                "message": f"Request failed: {e}"
            })

    @staticmethod
    def _get_table_parameter():
        """Method to get the table"""
        return RestService.request.GET.get('table', None)

    @staticmethod
    def _is_token_endpoint():
        """Method to determine if the endpoint is a token endpoint"""
        return RestService.get_endpoint() == 'get-csrf-token'

    @staticmethod
    def _query_requires_join():
        """Method to determine if a deep join is required"""
        endpoint = RestService.get_endpoint()
        table_name = RestService._get_table_parameter()

        if table_name:
            table_name = table_name.lower()

        return table_name and table_name != endpoint
