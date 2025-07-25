from django.apps import AppConfig
import threading
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth import get_user_model

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        def create_superuser_if_not_exists():
            try:
                User = get_user_model()
                if not User.objects.filter(username="drey").exists():
                    User.objects.create_superuser(
                        username="drey",
                        email="cobi658@gmail.com",
                        password="mikay2021"
                    )
            except (OperationalError, ProgrammingError):
                pass  # Database might not be ready yet — ignore and skip

        threading.Thread(target=create_superuser_if_not_exists).start()
