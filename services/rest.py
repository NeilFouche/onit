"""
On It REST Service

Handles REST API requests
"""

import json
import hashlib
import logging
import sys
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token


class RestService():
    """Handles REST API requests"""

    requests: dict[str, HttpRequest] = {}
    views = {}
    logger = logging.getLogger("django")
    control_parameters = []

    @staticmethod
    def remove_request(request_key: str):
        """Method to remove a request"""
        RestService.requests.pop(request_key, None)

    @staticmethod
    def error_response(error, status: int = 400):
        """Method to return an error response"""
        return JsonResponse({
            'success': False,
            'message': error,
        }, status=status)

    @staticmethod
    def get_context(request_key: str):
        """Gets the endpoint_context from the request path"""
        request = RestService.requests.get(request_key)
        if not request:
            raise ValueError("Unknown request. See docs for supported endpoints.")

        return request.GET.get('with_context')

    @staticmethod
    def get_token(request: HttpRequest):
        """Method to get the CSRF token"""
        return JsonResponse({'csrf_token': get_token(request)})

    @staticmethod
    def get_endpoint(request_key: str) -> str:
        """Method to get the endpoint"""
        request = RestService.requests.get(request_key)
        if request is None:
            raise ValueError("Unknown request. See docs for supported endpoints.")

        return request.path.strip('/')

    @staticmethod
    def get_command(request_key: str) -> str:
        """Gets the command of the request. Command is always the first item in the """
        request = RestService.requests.get(request_key)
        if not request:
            raise ValueError("Unknown request. See docs for supported endpoints.")

        # Return the first query parameter which is the command by design
        return next(iter(request.GET))

    @staticmethod
    def get_command_target(request_key: str):
        request = RestService.requests.get(request_key)
        if not request:
            raise ValueError("Unknown request. See docs for supported endpoints.")

        command = RestService.get_command(request_key)
        return request.GET[command]

    @staticmethod
    def get_control_parameters():
        config_path = "data/api_specifications/control_parameters.json"
        with open(config_path, 'r') as file:
            RestService.control_parameters = json.load(file)

    @staticmethod
    def hash_request(request: HttpRequest):
        """
        Method to get the hash

        The hash is generated based on the target table, starting table,
        and query parameters.

        Returns:
            str: The hashed key.
        """
        hash_object = hashlib.md5(json.dumps(
            obj=request.get_full_path()).encode('utf-8')
        )
        request_key = hash_object.hexdigest()

        if request_key in RestService.requests:
            return request_key

        RestService.requests[request_key] = request

        return request_key

    @staticmethod
    def get_query_parmeters(request_key: str):
        """Method to get the query parameters"""
        request = RestService.requests.get(request_key)
        if request is None:
            raise ValueError("Unknown request. See docs for supported endpoints.")

        command = RestService.get_command(request_key)
        return {
            key: value
            for key, value in request.GET.items() if key not in [command, *RestService.control_parameters]
        }

    @staticmethod
    def get_request(request_key: str) -> HttpRequest:
        """Returns a specific request"""
        request = RestService.requests.get(request_key)
        if request is None:
            raise ValueError("Unknown request. See docs for supported endpoints.")

        return RestService.requests[request_key]

    @staticmethod
    def get_request_body(request_key: str):
        """Method to get the request body"""
        request = RestService.requests.get(request_key)
        if request is None:
            raise ValueError("Unknown request. See docs for supported endpoints.")

        return request.body.decode('utf-8')

    @staticmethod
    def get_view(request_key: str):
        """Method to get the view"""
        if RestService._is_token_endpoint(request_key):
            return RestService.views['TOKEN:CSRF']

        request = RestService.requests.get(request_key)
        if request is None:
            raise ValueError("Unknown request. See docs for supported endpoints.")

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
    def response(request_key, data):
        """Method to return a response"""
        endpoint = RestService.get_endpoint(request_key)
        entities = RestService.get_query_parmeters(request_key)

        return JsonResponse({
            "message": f"{endpoint.title()} request processed succesfully",
            "status": 200,
            "endpoint": endpoint,
            "results": len(data) if data and isinstance(data, list) else 0,
            "size (bytes)": sys.getsizeof(data),
            "query parameters": entities,
            "data": data
        })

    @staticmethod
    def _is_token_endpoint(request_key: str):
        """Method to determine if the endpoint is a token endpoint"""
        return RestService.get_endpoint(request_key) == 'get-csrf-token'
