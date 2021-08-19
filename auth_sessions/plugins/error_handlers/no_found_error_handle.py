"""
Error handle for 404 Not Found Error.
"""
from django.http import JsonResponse


def no_found_error_handle(request, exception=None):
    """
    Standard Json response
    """
    return JsonResponse({"error": "The resource was not found"}, status=404)
