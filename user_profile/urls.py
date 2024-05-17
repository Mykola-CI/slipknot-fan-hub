from django.urls import path
from .views.profile import profile
from .views.playlists import (
    PlaylistCreateView,
    PlaylistCreatedView,
    PlaylistUpdateView,
    PlaylistDeleteView
)

urlpatterns = [
    path('', profile, name='profile'),
    path(
        'playlists/create/',
        PlaylistCreateView.as_view(),
        name='playlist_create'),
    path(
        'playlists/<int:pk>/create/created/',
        PlaylistCreatedView.as_view(),
        name='playlist_created'),
    path(
        'playlists/<int:pk>/update/',
        PlaylistUpdateView.as_view(),
        name='playlist_update'),
    path(
        'playlists/<int:pk>/update/updated/',
        PlaylistCreatedView.as_view(),
        name='playlist_updated'),
    path(
        'playlists/<int:pk>/delete/',
        PlaylistDeleteView.as_view(),
        name='playlist_delete'),
]
