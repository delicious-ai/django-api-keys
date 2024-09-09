from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from django_api_keys.package_settings import API_KEY_HEADER


def require_api_key(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get(API_KEY_HEADER)
        if not api_key:
            return JsonResponse({"error": _("API key is missing")}, status=400)

        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            raise PermissionDenied("Entity is not authenticated")

        if hasattr(request, "user") and not request.user.is_active:
            raise PermissionDenied("Entity associated with API Key is inactive")

        if hasattr(request, "auth_errors") and len(request.auth_errors) > 0:
            raise PermissionDenied(", ".join(request.auth_errors))

        return view_func(request, *args, **kwargs)

    return _wrapped_view
