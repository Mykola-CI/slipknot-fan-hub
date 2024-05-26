from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
from .models import PlaylistPost
from user_profile.models import Playlist, UserProfile, PlaylistItem


def home_view(request):
    playlist_posts = PlaylistPost.objects.all().order_by('-created_on')
    playlists = Playlist.objects.filter(playlist_post__isnull=False)

    # Pagination logic
    paginator = Paginator(playlist_posts, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'playlist_posts': paginated_posts,
        'playlists': playlists,
    }
    return render(request, 'core/home.html', context)


class PlaylistPostDetailView(DetailView):
    model = PlaylistPost
    template_name = 'core/playlistpost_detail.html'
    context_object_name = 'playlistpost'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.object.playlist
        context['playlist'] = playlist
        context['author_profile'] = UserProfile.objects.get(
            user=playlist.author
        )
        context['playlist_items'] = PlaylistItem.objects.filter(
            playlist=playlist
        )
        return context
