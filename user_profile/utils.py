from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Playlist


# Handle the form_valid method for views
def handle_form_valid(view, form):
    form.instance.author = view.request.user
    response = super(view.__class__, view).form_valid(form)
    messages.success(
        view.request,
        "You have successfully saved the changes"
    )
    return response


# Get the success URL for views
def get_success_url(view, reverse_path):
    return reverse(
        reverse_path,
        kwargs={'pk': view.object.id}
    )


class AuthorRequiredMixin:
    """
    Mixin to check if the user is the author of the playlist
    """
    def dispatch(self, request, *args, **kwargs):
        playlist_id = kwargs.get('pk')
        if not playlist_id:
            raise PermissionDenied("Playlist ID not provided")

        playlist = get_object_or_404(Playlist, pk=playlist_id)

        if not playlist.is_author(request.user):
            raise PermissionDenied(
                "You are not authorised to access this page"
            )

        return super().dispatch(request, *args, **kwargs)
