"""
api/views.py
Handling Requests from the frontend
"""

import json
import logging
from django.core.cache import cache
from django.conf import settings
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.shortcuts import redirect
from api.models import Employee, MediaAsset, Person, EntityMedia
from libs.strings import camel_to_snake
from services.database import DatabaseService
from services.data import DataService
from services.rest import RestService
from services.processing import TransformationService

logger = logging.getLogger("django")


@ensure_csrf_cookie
def view_manager(request: HttpRequest):
    """
    View to manage requests from the frontend
    The RestService will determine which view in this file to call and return
    the view to handle the request.
    """

    request_key = RestService.hash_request(request)
    view = RestService.get_view(request_key)

    return view(request_key)


###############################################################################
#                                 GET HANDLERS                                #
###############################################################################


@csrf_exempt
@RestService.register_view('TOKEN:CSRF')
def get_token(request_key):
    """
    View to handle GET requests for CSRF token
    """
    request = RestService.get_request(request_key)
    return RestService.get_token(request)


@RestService.register_view('GET')
def get_handler(request_key):
    """
    View to handle GET requests from the frontend
    """
    try:
        data = DataService.fetch_data(request_key)

        return RestService.response(request_key, data)
    except ValueError as e:
        return RestService.error_response(error=e)


###############################################################################
#                                POST HANDLERS                                #
###############################################################################


@transaction.atomic
@RestService.register_view('POST')
def post_handler(request_key):
    """
    View to handle POST requests from the frontend
    """
    try:
        request = RestService.get_request(request_key)
        if request:
            logger.info(f"Received cookies: {request.COOKIES}")

        # Set the request
        data = RestService.get_request_body(request_key)
        table_name = RestService.get_command_target(request_key)

        # Create the record
        onitdb = DatabaseService.get_database()
        table = onitdb.get(camel_to_snake(table_name))

        processor = TransformationService.get_processor(f"Create:{table_name}:Pre")
        preprocessed_data = processor.transform(data, request_key)

        data = table.create(preprocessed_data)

        processor = TransformationService.get_processor(f"Create:{table_name}:Post")
        preprocessed_data = processor.transform(data, request_key)

        return RestService.response(request_key, data)
    except ValueError as err:
        return RestService.error_response(error=err)


###############################################################################
#                                LANDING VIEW                                 #
###############################################################################


def index(request, *args, **kwargs):
    """
    View to handle requests to the root URL
    """
    if settings.ENV == 'production':
      return redirect("https://www.onitafrica.com/")

    return redirect("cb/health/")


###############################################################################
#                                HEALTH VIEW                                  #
###############################################################################


def health_check(request, *args, **kwargs):
    """
    View to handle requests to the root URL
    """
    return JsonResponse({"status": "ok"})


###############################################################################
#                                CLEAR CACHE                                  #
###############################################################################


def clear_cache(request, *args, **kwargs):
    """
    View to handle requests to the root URL
    """
    cache.clear()
    return JsonResponse({"message": "Cache cleared"})


###############################################################################
#                                  TEST VIEW                                  #
###############################################################################


def backend_test(request, *args, **kwargs):
    request_key = RestService.hash_request(request)
    return JsonResponse({"hash": request_key})


def test_view(request, request_key=None):
    """
    View to handle test requests from the frontend
    """
    request_key = RestService.hash_request(request)

    # Select related entities
    data = EntityMedia.objects.filter(object_id__in=1, content_type__model='service')

    return RestService.response(request_key, data=list(data.values()))
