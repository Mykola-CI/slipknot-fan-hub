from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    # for large numbers of users:
    default_auto_field = 'django.db.models.BigAutoField'
    # name of Django application
    name = 'user_profile'

    def ready(self):
        import user_profile.signals  # noqa: F401
