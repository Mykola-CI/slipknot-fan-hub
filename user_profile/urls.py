from django.urls import path
from .views import profile, PlaylistCreateView, PlaylistCreatedView

urlpatterns = [
    path('', profile, name='profile'),
    path(
        'playlists/create/',
        PlaylistCreateView.as_view(),
        name='playlist_create'),
    path(
        'playlists/<int:playlist_id>/create/created/',
        PlaylistCreatedView.as_view(),
        name='playlist_created'),
]
