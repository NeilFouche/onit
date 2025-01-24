"""
On It REST Service

Handles REST API requests
"""

import json
import hashlib
import logging
import sys
from django.http import JsonResponse
from django.middleware.csrf import get_token
from libs.strings import camel_to_snake, kebab_to_camel


class RestService():
    """Handles REST API requests"""

    requests = {}
    views = {}
    logger = logging.getLogger("django")

    @staticmethod
    def remove_request(hash_key):
        """Method to remove a request"""
        RestService.requests.pop(hash_key, None)

    @staticmethod
    def error_response(error, status=400):
        """Method to return an error response"""
        return JsonResponse({
            'success': False,
            'message': error,
        }, status=status)

    @staticmethod
    def extract_context(request):
        """Method to extract the context"""
        path = request.path.rstrip('/')
        path_parts = path.split('/')
        return path_parts[-1] if len(path_parts) > 2 else None

    @staticmethod
    def get_token(request):
        """Method to get the CSRF token"""
        return JsonResponse({'csrf_token': get_token(request)})

    @staticmethod
    def get_endpoint(hash_key):
        """Method to get the endpoint"""
        request = RestService.requests.get(hash_key)
        path = request.path.rstrip('/')
        path_parts = path.split('/')
        return path_parts[2]

    @staticmethod
    def get_context(hash_key):
        """Method to get context if provided"""
        request = RestService.requests.get(hash_key)
        return RestService.extract_context(request)

    @staticmethod
    def hash_request(request):
        """
        Method to get the hash

        The hash is generated based on the target table, starting table,
        and query parameters.

        Returns:
            str: The hashed key.
        """
        RestService.logger.debug("==> 1")
        hash_object = hashlib.md5(json.dumps(
            obj=request.get_full_path()).encode('utf-8')
        )
        hash_key = hash_object.hexdigest()

        RestService.logger(f"==> 2 ==> {hash_key}")

        if hash_key in RestService.requests:
            return hash_key

        RestService.requests[hash_key] = request

        return hash_key

    @staticmethod
    def get_message(data, table_name):
        """Method to get the message"""
        return "No records found" if not data else f"{table_name} records retrieved succesfully"

    @staticmethod
    def get_query_parmeters(hash_key):
        """Method to get the query parameters"""
        request = RestService.requests.get(hash_key)
        return {
            key: value
            for key, value in request.GET.items() if key != 'table'
        }

    @staticmethod
    def get_request_body(hash_key):
        """Method to get the request body"""
        request = RestService.requests.get(hash_key)
        return request.body.decode('utf-8')

    @staticmethod
    def get_starting_table(hash_key):
        """Method to get the starting table"""
        return RestService._get_table_parameter(hash_key)

    @staticmethod
    def get_target_table(hash_key):
        """Method to get the target table"""
        return kebab_to_camel(RestService.get_endpoint(hash_key))

    @staticmethod
    def get_table_name(hash_key):
        """
        Method to get the table name

        Note: If the table name is not provided as a query parameter, use the endpoint.

        Returns:
            str: The table name converted to snake_case.
        """
        table_name = RestService._get_table_parameter(hash_key)
        if not table_name:
            table_name = RestService.get_endpoint(hash_key)

        return camel_to_snake(table_name)

    @staticmethod
    def get_view(hash_key):
        """Method to get the view"""
        if RestService._is_token_endpoint(hash_key):
            return RestService.views['get_token']

        request = RestService.requests.get(hash_key)

        return RestService.views[request.method]

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
    def response(hash_key, data):
        """Method to return a response"""
        try:
            table = RestService.get_table_name(hash_key)
            message = RestService.get_message(data, table.title())
            entities = RestService.get_query_parmeters(hash_key)

            return JsonResponse({
                "message": message,
                "status": 200,
                "table": table,
                "results": len(data) if data and isinstance(data, list) else 0,
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
    def _get_table_parameter(hash_key):
        """Method to get the table"""
        request = RestService.requests.get(hash_key)
        return request.GET.get('table', None)

    @staticmethod
    def _is_token_endpoint(hash_key):
        """Method to determine if the endpoint is a token endpoint"""
        return RestService.get_endpoint(hash_key) == 'get-csrf-token'

    @staticmethod
    def _query_requires_join(hash_key):
        """Method to determine if a deep join is required"""
        endpoint = RestService.get_endpoint(hash_key)
        table_name = RestService._get_table_parameter(hash_key)

        if table_name:
            table_name = table_name.lower()

        return table_name and table_name != endpoint
