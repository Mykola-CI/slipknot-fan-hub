from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    # for big numbers of users:
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'

    def ready(self):
        import user_profile.signals  # noqa: F401
