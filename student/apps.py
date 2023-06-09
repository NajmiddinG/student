from django.apps import AppConfig
from django.core.management import call_command
from django.utils import timezone


class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'
