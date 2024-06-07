from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PlaylistPost, Comment
from user_profile.models import Playlist, UserProfile, PlaylistItem
from .forms import CommentForm


# Apart from general context creates dynamic blog post context with pagination
def home_view(request):
    # Annotating each PlaylistPost with the count of related comments
    playlist_posts = PlaylistPost.objects.annotate(
        comment_count=Count('comments')).order_by('-created_on')

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


class PlaylistPreviewView(TemplateView):
    """
    Creating context and view for the full list of shared playlists page.
    """

    template_name = 'core/playlist_preview.html'
    context_object_name = 'playlist_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetching all PlaylistPost objects ordered by '-created_on'
        # and select related Playlist objects
        playlist_posts = PlaylistPost.objects.select_related(
            'playlist').order_by('-created_on')

        # Adding PlaylistPost objects to the context
        context['playlist_posts'] = playlist_posts

        return context


# Creating context for author presentation page with info and playlists
def user_profile_presentation(request, username):
    user_profile = get_object_or_404(
        UserProfile.objects.select_related('user'), user__username=username)
    profile_user = user_profile.user
    playlists = Playlist.objects.filter(author=profile_user, status=1)

    # Create a list comprehension to hold playlists with their associated
    # PlaylistPost pk. The goal is to avoid creation of extra views and
    # templates and enable user to access the existing PlaylistPost detail view
    playlist_with_posts = [
        {
            'playlist': playlist,
            'playlist_post_slug': (
                PlaylistPost.objects.get(playlist=playlist).slug)
        }
        for playlist in playlists
    ]

    return render(
        request,
        'core/user_profile_presentation.html',
        {'profile_user': profile_user,
         'user_profile': user_profile,
         'playlist_with_posts': playlist_with_posts}
    )


class PlaylistPostDetailView(DetailView):
    """
    Display a Playlist Detail view selected on the home page.
    Creating contexts: playlists, playlist items, author's profile,
    comments, comment count and comment form

    """
    model = PlaylistPost
    template_name = 'core/playlist_post_detail.html'
    context_object_name = 'playlist_post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.object.playlist
        user = self.request.user

        # Adding playlist, author profile, and playlist items to context
        context['playlist'] = playlist
        context['author_profile'] = UserProfile.objects.get(
            user=playlist.author)
        context['playlist_items'] = PlaylistItem.objects.filter(
            playlist=playlist)

        # Adding comments and comment form to context
        comments = self.object.comments.all()

        # Check if the current user has liked the comment (False or True)
        for comment in comments:
            comment.is_liked_by_user = user

        comment_count = comments.count()
        comment_form = CommentForm()

        context['comments'] = comments
        context['comment_count'] = comment_count
        context['comment_form'] = comment_form

        # Check if the current user has liked the playlist_post (False or True)
        context['liked'] = self.object.likes.filter(id=user.id).exists()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.playlist_post = self.object
            new_comment.author = request.user
            new_comment.save()
            return redirect('playlist_post_detail', slug=self.object.slug)
        else:
            context = self.get_context_data()
            context['comment_form'] = comment_form
            return self.render_to_response(context)


def comment_edit(request, slug, comment_id):
    """
    Display an individual comment for edit.

    """
    post = get_object_or_404(PlaylistPost, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating comment!')

    return HttpResponseRedirect(reverse('playlist_post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comments
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('playlist_post_detail', args=[slug]))


@login_required
def like_view(request, slug):
    post = get_object_or_404(PlaylistPost, slug=slug)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('playlist_post_detail', args=[slug]))


@login_required
def like_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.likes_comment.filter(id=request.user.id).exists():
        comment.likes_comment.remove(request.user)
    else:
        comment.likes_comment.add(request.user)

    return redirect(reverse('playlist_post_detail', args=[slug]))
