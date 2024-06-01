from django.urls import path
from .views import moderator_section_view


urlpatterns = [
    path(
        "moderator-section/",
        moderator_section_view,
        name="moderator_section",
    )
]
