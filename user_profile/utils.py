from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Playlist, PlaylistItem


# Custom validator to prevent forced messages from Cloudinary
# even before image or other files handled by widgets
def validate_file_size(value, max_size):
    if value.size > max_size:
        raise ValidationError(
            f"Your file size {value.size} bytes is too large. "
            f"Max allowed size is {max_size} bytes."
        )


# Custom override of the form_valid method to ensure the author field remains
# consistent and accurate each time when saving the form + success message
def handle_form_valid(view, form, message):
    form.instance.author = view.request.user
    response = super(view.__class__, view).form_valid(form)
    messages.success(
        view.request,
        message,
    )
    return response


# Custom override of success_url to pass playlist ID
def get_success_url(view, reverse_path):
    return reverse(
        reverse_path,
        kwargs={'pk': view.object.id}
    )


class AuthorRequiredMixin:
    """
    Mixin to check if the user is the author of the playlist or playlist item.
    """
    def dispatch(self, request, *args, **kwargs):
        # Determine if the view is for a Playlist or PlaylistItem
        if hasattr(self, 'model') and self.model == PlaylistItem:
            playlist_item_id = kwargs.get('pk')
            if not playlist_item_id:
                raise PermissionDenied("Playlist Item ID not provided")

            playlist_item = get_object_or_404(
                PlaylistItem, pk=playlist_item_id)
            playlist = playlist_item.playlist
        else:
            playlist_id = kwargs.get('pk')
            if not playlist_id:
                raise PermissionDenied("Playlist ID not provided")

            playlist = get_object_or_404(Playlist, pk=playlist_id)

        if not playlist.is_author(request.user):
            raise PermissionDenied(
                "You are not authorised to access this page")

        return super().dispatch(request, *args, **kwargs)
