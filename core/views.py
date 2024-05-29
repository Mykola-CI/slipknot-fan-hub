from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PlaylistPost, Comment
from user_profile.models import Playlist, UserProfile, PlaylistItem
from .forms import CommentForm


# Apart from general context creates dynamic blog context with pagination
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
    """
    Display a Playlist Detail view selected on the home page.
    Creating contexts: playlists, playlist items, author's profile,
    comments, comment count and comment form

    """
    model = PlaylistPost
    template_name = 'core/playlist_post_detail.html'
    context_object_name = 'playlist_post'

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
            return redirect('playlist_post_detail', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = comment_form
            return self.render_to_response(context)


def comment_edit(request, pk, comment_id):
    """
    Display an individual comment for edit.

    """
    if request.method == "POST":

        queryset = PlaylistPost.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        comment = get_object_or_404(Comment, pk=comment_id)
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

    return HttpResponseRedirect(reverse('playlist_post_detail', args=[pk]))


def comment_delete(request, pk, comment_id):
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

    return HttpResponseRedirect(reverse('playlist_post_detail', args=[pk]))


@login_required
def like_view(request, pk):
    post = get_object_or_404(PlaylistPost, pk=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('playlist_post_detail', args=[pk]))


@login_required
def like_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.likes_comment.filter(id=request.user.id).exists():
        comment.likes_comment.remove(request.user)
    else:
        comment.likes_comment.add(request.user)

    return redirect(reverse('playlist_post_detail', args=[pk]))
