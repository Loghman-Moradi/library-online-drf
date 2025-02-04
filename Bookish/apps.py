from django.apps import AppConfig


class BookishConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bookish'

    def ready(self):
        import Bookish.signals
