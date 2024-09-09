from django.http import JsonResponse
from django.views.decorators.http import require_GET

from django_api_keys.decorators import require_api_key


@require_GET
@require_api_key
def get_fruits(request):
    return JsonResponse({"detail": True})
