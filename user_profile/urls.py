from django.urls import path
from .views import profile, PlaylistCreateView, PlaylistItemCreateView

urlpatterns = [
    path('', profile, name='profile'),
    path(
        'playlists/create/',
        PlaylistCreateView.as_view(),
        name='playlist_create'),
    path(
        'playlists/<int:playlist_id>/items/create/',
        PlaylistItemCreateView.as_view(),
        name='playlist_item_create'),
]
