from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import PlaylistPost
from user_profile.models import Playlist


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
