from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user_profile.views.error_views import my_custom_permission_denied_view
from django_summernote.views import SummernoteUploadAttachment

handler403 = my_custom_permission_denied_view

urlpatterns = [
    path("", include("core.urls"), name="core-urls"),
    path("profile/", include("user_profile.urls"), name="profile-urls"),
    path("moderator/", include("moderator.urls"), name="moderator-urls"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('summernote/', include('django_summernote.urls')),
    path(
        'summernote/upload_attachment/',
        SummernoteUploadAttachment.as_view(),
        name='django_summernote-upload_attachment'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
