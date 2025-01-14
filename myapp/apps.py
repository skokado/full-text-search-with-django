from django.apps import AppConfig
from opensearchpy import connections


class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"
