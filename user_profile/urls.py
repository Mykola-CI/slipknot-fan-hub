from django.urls import path
from .views import (
    profile,
    PlaylistCreateView,
    PlaylistCreatedView,
    PlaylistUpdateView
)

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
    path(
        'playlists/<int:pk>/update/',
        PlaylistUpdateView.as_view(),
        name='playlist_update'),
    path(
        'playlists/<int:playlist_id>/update/updated/',
        PlaylistCreatedView.as_view(),
        name='playlist_updated'),
]
