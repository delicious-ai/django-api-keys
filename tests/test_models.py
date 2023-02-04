import pytest

from rest_framework_simple_api_key.models import APIKey
from .fixtures.user import user
from .fixtures.api_key import active_api_key

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestApiKeyModel:
    pytestmark = pytest.mark.django_db

    def test_create_key(self, user):
        data = {
            "entity": user,
        }
        api_key, key = APIKey.objects.create_key(**data)

        assert type(key) is str

        assert api_key.entity.pk == user.pk
        assert not api_key.revoked
        assert api_key.expiry_date

    def test_get_key(self, active_api_key):
        api_key, _ = active_api_key

        api_key_pk = api_key.pk

        obj = APIKey.objects.get_api_key(api_key_pk)
        assert obj

    def test_revoke_keys(self, active_api_key):
        api_key, _ = active_api_key

        APIKey.objects.revoke_api_key(api_key.pk)

        api_key.refresh_from_db()

        assert api_key.revoked
