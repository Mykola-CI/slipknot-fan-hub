from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user_profile.views.error_views import my_custom_permission_denied_view


handler403 = my_custom_permission_denied_view

urlpatterns = [
    path("", include("core.urls"), name="core-urls"),
    path("profile/", include("user_profile.urls"), name="profile-urls"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        '/static/ckeditor/', document_root=settings.STATIC_ROOT + '/ckeditor/'
        )
