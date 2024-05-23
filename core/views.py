from django.shortcuts import render
from .models import PlaylistPost
from user_profile.models import Playlist, UserProfile


def home_view(request):
    playlist_posts = PlaylistPost.objects.all().order_by('-created_on')
    playlists = Playlist.objects.filter(playlist_post__isnull=False)
    context = {
        'playlist_posts': playlist_posts,
        'playlists': playlists,
    }
    return render(request, 'core/home.html', context)
