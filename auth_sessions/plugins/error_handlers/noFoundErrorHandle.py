from django.http import JsonResponse


def no_found_error_handle(request, exception=None):
    return JsonResponse({
        'error': 'The resource was not found'
    }, status=404)
