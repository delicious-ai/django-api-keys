import typing

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from django_api_keys import package_settings


class APIKeyParser:
    """
    This is a custom parser used to retrieve the API Key from the
    authorization header. You can add custom parsing validation here.
    """

    keyword = package_settings.API_KEY_HEADER
    message = "No API key provided."

    def get(self, request: HttpRequest) -> typing.Optional[str]:
        return self.get_from_authorization(request)

    def get_from_authorization(self, request: HttpRequest) -> typing.Optional[str]:
        key = self.get_from_header(request, self.keyword)

        if not key:
            raise PermissionDenied(self.message)
        return key

    def get_from_header(self, request: HttpRequest, name: str) -> typing.Optional[str]:
        return request.META.get(name) or None
