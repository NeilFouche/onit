"""
Helper functions for AWS Lambda functions
"""

import json


def get_batch_items(response: dict, table_name: str) -> tuple[list[dict], int]:
    """
    Checks if the response contains valid data and returns table items if it exists
    """
    if not response or "Responses" not in response:
        return [], 0

    responses = response.get("Responses", None)
    if table_name not in responses.keys():
        return [], 0

    return responses[table_name], len(responses[table_name])


def get_scan_items(response: dict) -> tuple[list[dict], int]:
    """
    Checks if the response contains valid data and returns table items if it exists
    """
    if not response:
        return [], 0

    return response.get("Items", None), response.get("Count", None)


def get_value(item: dict, key: str, data_type: str):
    return item.get(key, {}).get(data_type) or None


def get_query_params(event: dict, search_params: list) -> dict:
    """
    The backend allows for variations of the query keys (e.g. service, services)
    The function will try the items in [search_params] until it finds a match. Then
    return a dict with the provided parameter and values.

    Args:
        event (dict): The input data corresponding to the AWS service that invokes the Lambda function
        search_params: List of valid query parameters

    Returns:
        (dict): {query parameter: query values}
    """

    if not search_params:
        return None, None

    if not isinstance(search_params, list):
        search_params = [search_params]

    if not event or "queryStringParameters" not in event.keys():
        return None, None

    query_params = event.get("queryStringParameters", {})
    for parameter in search_params:
        values = query_params.get(parameter, None)
        if values:
            return parameter, values.split(',')

    return None, None


def error_response(error_label: str, error_detail, status: int) -> dict:
    """
    Creates an error response with the error message and status code
    """

    return {
        "statusCode": status,
        "body": json.dumps({
            "success": False,
            "message": f"{error_label}: {str(error_detail)}"
        })
    }
