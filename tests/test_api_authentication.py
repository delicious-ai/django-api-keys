import pytest

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory

from django_api_keys import package_settings

from .fixtures.user import user
from .fixtures.api_key import expired_api_key, active_api_key, revoked_api_key

pytestmark = pytest.mark.django_db


@pytest.fixture
def invalid_request(user):
    factory = RequestFactory()
    return factory.get("/test-request/")


@pytest.fixture
def invalid_request_with_expired_api_key(user, expired_api_key):
    factory = RequestFactory()
    _, key = expired_api_key

    return factory.get(
        "/test-request/",
        HTTP_X_API_KEY=key,
    )


@pytest.fixture
def invalid_request_with_revoked_api_key(user, revoked_api_key):
    factory = RequestFactory()
    _, key = revoked_api_key

    return factory.get("/test-request/", HTTP_X_API_KEY=key)


@pytest.fixture
def valid_request(user, active_api_key):
    factory = RequestFactory()
    _, key = active_api_key
    return factory.get("/test-request/", HTTP_X_API_KEY=key)


def api_key_authentication():
    from django_api_keys.backends import APIKeyAuthenticationBackend

    return APIKeyAuthenticationBackend()


@pytest.mark.django_db
class TestAPIKeyAuthenticationBackend:
    pytestmark = pytest.mark.django_db

    def test_get_key(self, valid_request):
        key = api_key_authentication().get_key(valid_request)
        assert type(key) is str

    def test_authenticate_valid_request(self, valid_request):
        entity = api_key_authentication().authenticate(valid_request)
        assert isinstance(entity, User)

    def test_authenticate_invalid_request(self, invalid_request):
        entity = None
        message = "No API key provided"
        errors = []
        entity = api_key_authentication().authenticate(invalid_request, errors=errors)

        assert entity is None
        assert errors == [message]

    def test_authenticate_invalid_request_with_expired_key(
        self, invalid_request_with_expired_api_key
    ):
        entity = None
        message = "API Key has already expired"
        errors = []
        entity = api_key_authentication().authenticate(
            invalid_request_with_expired_api_key, errors=errors
        )

        assert entity is None
        assert errors == [message]

    def test_authenticate_invalid_request_with_revoked_key(
        self, invalid_request_with_revoked_api_key
    ):
        entity = None
        message = "This API Key has been revoked"
        errors = []
        entity = api_key_authentication().authenticate(
            invalid_request_with_revoked_api_key, errors=errors
        )

        assert entity is None
        assert errors == [message]
