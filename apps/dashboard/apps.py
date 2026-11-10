import os
from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    
    #To create super user automatically on deployment
    def ready(self):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if username and password:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email or '',
                        password=password
                    )
            except (OperationalError, ProgrammingError):
                # Skips safely during collectstatic before tables exist
                pass
