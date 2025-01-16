from django.db import transaction
from django.http import JsonResponse
from .models import Sequence


def get_next_sequence(entity_type):
    """A function that retrieves and updates the entity_type sequence"""
    with transaction.atomic():
        sequence, _ = Sequence.objects.get_or_create(
            entity_type=entity_type,
            defaults={'current_value': 0}
        )
        sequence.current_value += 1
        sequence.save()
        return sequence.current_value


def response_error(msg, status):
    """A function that returns a JSON response with an error message"""

    return JsonResponse({
        'success': False,
        'message': msg,
    }, status=status)
