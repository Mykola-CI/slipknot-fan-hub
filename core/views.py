from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
from .models import PlaylistPost
from user_profile.models import Playlist, UserProfile, PlaylistItem
from .forms import CommentForm


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
    template_name = 'core/playlist_post_detail.html'
    context_object_name = 'playlist_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.object.playlist
        context['playlist'] = playlist
        context['author_profile'] = UserProfile.objects.get(
            user=playlist.author)
        context['playlist_items'] = PlaylistItem.objects.filter(
            playlist=playlist)

        # Adding comments and comment form to context
        comments = self.object.comments.all()
        comment_count = comments.count()
        comment_form = CommentForm()

        context['comments'] = comments
        context['comment_count'] = comment_count
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.playlist_post = self.object
            new_comment.author = request.user
            new_comment.save()
            return redirect('playlist_post_detail', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = comment_form
            return self.render_to_response(context)
