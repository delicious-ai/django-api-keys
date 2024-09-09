from django.apps import AppConfig


class RotationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_api_keys.rotation"
    label = "django_api_keys_rotation"
