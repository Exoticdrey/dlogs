from django.apps import AppConfig
from django.db.utils import OperationalError
from django.db import connections
from django.contrib.auth import get_user_model

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        User = get_user_model()
        try:
            # Check if the auth_user table exists
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT 1 FROM auth_user LIMIT 1")
            
            # If the user doesn't exist, create the superuser
            if not User.objects.filter(username="drey").exists():
                User.objects.create_superuser("drey", "cobi658@gmail.com", "mikay2021")
        except OperationalError:
            # If the database isn't ready yet, do nothing
            pass
