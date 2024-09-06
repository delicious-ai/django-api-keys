from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def get_fruits(request):
    return JsonResponse({"detail": True})
