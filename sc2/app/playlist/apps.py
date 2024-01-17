from django.apps import AppConfig


class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'playlist'

    def ready(self):
        import playlist.signals # noqa
