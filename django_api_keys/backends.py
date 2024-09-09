import typing

from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist


from django_api_keys.crypto import get_crypto
from django_api_keys.models import APIKey
from django_api_keys.parser import APIKeyParser


class APIKeyAuthentication(BaseBackend):
    model = APIKey
    key_parser = APIKeyParser()

    def __init__(self):
        self.key_crypto = get_crypto()

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        return self.key_parser.get(request)

    def authenticate(self, request, **kwargs):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires api key authentication.
        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
        this means we know authentication will fail. An example of
        this is when the request does not include an api key in the
        headers.

        2) `(entity)` - We return an entity object when
        authentication is successful.
        If neither case is met, that means there's an error,
        and we do not return anything.
        """

        errors = kwargs.pop("errors", [])
        try:
            key = self.get_key(request)
        except PermissionDenied:
            errors.append("No API key provided")
            return None

        return self._authenticate_credentials(request, key, errors, **kwargs)

    def _authenticate_credentials(self, request, key: str, errors: list[str]):
        key_crypto = self.key_crypto

        try:
            payload = key_crypto.decrypt(key)
        except ValueError:
            errors.append("Invalid API Key")

        if "_pk" not in payload or "_exp" not in payload:
            errors.append("Invalid API Key")

        if payload["_exp"] < now().timestamp():
            errors.append("API Key has already expired")
        try:
            api_key = self.model.objects.get(id=payload["_pk"])
        except ObjectDoesNotExist:
            errors.append("No entity matching this api key")

        if api_key.revoked:
            errors.append("This API Key has been revoked")

        if len(errors) > 0:
            return None
        return api_key.entity

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass
