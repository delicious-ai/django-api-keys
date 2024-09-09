from django.contrib.auth import authenticate


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, "user") or request.user.is_anonymous:
            errors = []
            user = authenticate(request=request, errors=errors)
            if user:
                request.user = request._cached_user = user
            request.auth_errors = errors
        response = self.get_response(request)

        return response
