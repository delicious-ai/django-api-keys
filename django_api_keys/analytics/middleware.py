from django_api_keys.analytics.models import ApiKeyAnalytics
from django_api_keys.crypto import get_crypto
from django_api_keys.parser import APIKeyParser
from django_api_keys.utils import get_key


class ApiKeyAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        key = get_key(APIKeyParser(), request)

        payload = get_crypto().decrypt(key)

        # Use the custom manager to handle endpoint access logging
        ApiKeyAnalytics.objects.add_endpoint_access(
            api_key_id=payload["_pk"], endpoint=request.path
        )

        return response
