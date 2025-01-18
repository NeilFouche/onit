"""
api/views.py
Handling Requests from the frontend
"""

from django.views.decorators.csrf import csrf_exempt
from api.models import Employee, MediaAsset
from services.cache import CacheService
from services.database import DatabaseService, Query
from services.rest import RestService


def view_manager(request):
    """
    View to manage requests from the frontend
    The RestService will determine which view in this file to call and return
    the view to handle the request.
    """

    hash_key = RestService.hash_request(request)
    view = RestService.get_view(hash_key)

    return view(request)


###############################################################################
#                                 GET HANDLERS                                #
###############################################################################


@csrf_exempt
@RestService.register_view('get_token')
def get_token(request):
    """
    View to handle GET requests for CSRF token
    """
    return RestService.get_token(request)


@RestService.register_view('GET')
def get_view(request):
    """
    View to handle GET requests from the frontend
    """
    try:
        # Set the request
        hash_key = RestService.hash_request(request)

        # Get the requested records
        data = CacheService.get_object(hash_key)
        if not data:
            onitdb = DatabaseService.get_database()
            data = onitdb.fetch_data(
                target=RestService.get_target_table(hash_key),
                source=RestService.get_starting_table(hash_key),
                filter_params=RestService.get_query_parmeters(hash_key),
                hash_key=hash_key
            )
            CacheService.set_object(hash_key, data)

        return RestService.response(hash_key, data)
    except ValueError as e:
        return RestService.error_response(error=e)


###############################################################################
#                                POST HANDLERS                                #
###############################################################################


@RestService.register_view('post_view')
def post_view(request):
    """
    View to handle POST requests from the frontend
    """
    try:
        # Set the request
        hash_key = RestService.hash_request(request)
        data = RestService.get_request_body(hash_key)
        table_name = RestService.get_table_name(hash_key)

        # Create the record
        onitdb = DatabaseService.get_database()
        table = onitdb.get_table(table_name)
        data = table.create(data)

        return RestService.response(hash_key, data)
    except ValueError as error:
        return RestService.error_response(error)


###############################################################################
#                                  TEST VIEW                                  #
###############################################################################


def test_view(request):
    """
    View to handle test requests from the frontend
    """
    hash_key = RestService.hash_request(request)

    # Select related entities
    related_entity = Employee
    related_entity_type = "employee"
    query_parameters = {"key": "oi-002"}

    # right set ------------------------v
    intermediate_values = related_entity.objects.\
        filter(**query_parameters).\
        values_list("id", flat=True)

    # Filter target entities
    target = MediaAsset
    target_related_name = "mediaentities"  # defined on table

    filter_parameters = {
        f"{target_related_name}__content_type__model": related_entity_type,
        f"{target_related_name}__object_id__in": intermediate_values
    }

    # left set --v
    data = target.objects.filter(**filter_parameters)

    CacheService.clear_cache()
    CacheService.clear_object_cache()

    return RestService.response(list(data.values()))
