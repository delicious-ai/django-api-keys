from datetime import timedelta
from django.conf import settings

DEFAULTS = {
    "FERNET_SECRET": "d-16UOyaBDFFmsD3k6JGfyBO8ccctQgcthul7OGIfx4=",
    "ROTATION_FERNET_SECRET": "",
    "API_KEY_LIFETIME": 365,
    "AUTHENTICATION_KEYWORD_HEADER": "X-Api-Key",
    "ROTATION_PERIOD": timedelta(days=7),
    "API_KEY_CLASS": "django_api_keys.Apikey",
}

USER_OVERRIDES = getattr(settings, "API_KEY_SETTINGS", {})


def resolved_value(key: str):
    return USER_OVERRIDES.get(key, DEFAULTS.get(key))


FERNET_SECRET = resolved_value("FERNET_SECRET")
ROTATION_FERNET_SECRET = resolved_value("ROTATION_FERNET_SECRET")
API_KEY_LIFETIME = resolved_value("API_KEY_LIFETIME")
AUTHENTICATION_KEYWORD_HEADER = resolved_value("AUTHENTICATION_KEYWORD_HEADER")
ROTATION_PERIOD = resolved_value("ROTATION_PERIOD")
API_KEY_CLASS = resolved_value("API_KEY_CLASS")
