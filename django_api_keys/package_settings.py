from datetime import timedelta
from django.conf import settings

DEFAULTS = {
    "FERNET_SECRET": "",
    "ROTATION_FERNET_SECRET": "",
    "API_KEY_LIFETIME": 365,
    "API_KEY_HEADER": "HTTP_X_API_KEY",
    "ROTATION_PERIOD": timedelta(days=7),
    "API_KEY_CLASS": "django_api_keys.Apikey",
}

USER_OVERRIDES = getattr(settings, "API_KEY_SETTINGS", {})


def resolved_value(key: str):
    return USER_OVERRIDES.get(key, DEFAULTS.get(key))


FERNET_SECRET = resolved_value("FERNET_SECRET")
ROTATION_FERNET_SECRET = resolved_value("ROTATION_FERNET_SECRET")
API_KEY_LIFETIME = resolved_value("API_KEY_LIFETIME")
API_KEY_HEADER = resolved_value("API_KEY_HEADER")
ROTATION_PERIOD = resolved_value("ROTATION_PERIOD")
API_KEY_CLASS = resolved_value("API_KEY_CLASS")
