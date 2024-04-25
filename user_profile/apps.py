from django.apps import AppConfig


class UserProfileConfig(AppConfig):

    # name of Django application
    name = 'user_profile'

    def ready(self):
        import user_profile.signals  # noqa: F401
