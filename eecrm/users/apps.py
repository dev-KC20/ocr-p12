import base.constants as cts
from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = cts.APPS_VERBOSE_NAME
