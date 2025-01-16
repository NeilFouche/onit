"""
front/views.py
Handling Requests from the frontend
"""

from django.views.decorators.csrf import csrf_exempt
from front.models import Employee, MediaAsset, ServiceMethod
from services.cache import CacheService
from services.database import DatabaseService, Query
from services.transformer import TransformerService
from services.rest import RestService


def view_manager(request):
    """
    View to manage requests from the frontend
    The RestService will determine which view in this file to call and return
    the view to handle the request.
    """

    RestService.request = request
    view = RestService.get_view()

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
        RestService.request = request

        hashed_key = RestService.get_hash()

        # Get the requested records
        data = CacheService.get_object(hashed_key)
        if not data:
            onitdb = DatabaseService.get_database()
            data = onitdb.fetch_data(
                target=RestService.get_target_table(),
                source=RestService.get_starting_table(),
                filter_params=RestService.get_query_parmeters()
            )
            CacheService.set_object(hashed_key, data)

        return RestService.response(data)
    except ValueError as e:
        return RestService.error_response(error=e)


@RestService.register_view('get_shallow_view')
def get_shallow_view(request):
    """
    View to handle GET requests from the frontend
    """
    try:
        # Set the request
        RestService.request = request
        table_name = RestService.get_table_name()
        hashed_key = RestService.get_hash()

        # Get the requested records
        data = CacheService.get_object(hashed_key)
        if not data:
            onitdb = DatabaseService.get_database()
            table = onitdb.get_table(table_name)
            query = Query.build(
                query_parameters=RestService.get_query_parmeters()
            )
            data = table.filter(query)
            CacheService.set_object(hashed_key, data)

        return RestService.response(data)
    except ValueError as e:
        return RestService.error_response(error=e)


@RestService.register_view('get_deep_view')
def get_deep_view(request):
    """
    View to handle GET requests from the frontend that require a deep join
    """
    try:
        # Set the request
        RestService.request = request
        query_parameters = RestService.get_query_parmeters()
        hashed_key = RestService.get_hash()

        # Get the requested records
        data = CacheService.get_object(hashed_key)
        if not data:
            onitdb = DatabaseService.get_database()
            query_path = onitdb.get_query_path(
                start_table=RestService.get_starting_table(),
                end_table=RestService.get_target_table()
            )
            data = onitdb.fetch_data(query_path, query_parameters)
            CacheService.set_object(hashed_key, data)

        return RestService.response(data)
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
        RestService.request = request
        data = RestService.get_request_body()
        table_name = RestService.get_table_name()

        # Create the record
        onitdb = DatabaseService.get_database()
        table = onitdb.get_table(table_name)
        data = table.create(data)

        return RestService.response(data)
    except ValueError as error:
        return RestService.error_response(error)


def test_view(request):
    """
    View to handle test requests from the frontend
    """
    RestService.request = request

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
