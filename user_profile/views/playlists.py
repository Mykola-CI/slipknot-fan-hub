from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView
)
from ..forms.playlist_forms import PlaylistForm
from ..models import Playlist, PlaylistItem
from ..utils import handle_form_valid, get_success_url, AuthorRequiredMixin


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'user_profile/playlist_form.html'

    # Set the author of the playlist to the current user and validates the form
    def form_valid(self, form):
        # call the handle_form_valid function from utils.py
        return handle_form_valid(
            self, form, "You have successfully created a new playlist")

    # Redirect to the playlist_created page for the new playlist
    def get_success_url(self):
        # call the get_success_url function from utils.py
        return get_success_url(self, 'playlist_created')


class PlaylistCreatedView(
        LoginRequiredMixin,
        AuthorRequiredMixin,
        TemplateView):

    template_name = 'user_profile/playlist_created.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Getting the playlist based on the passed 'pk'
        playlist_id = self.kwargs.get('pk')
        playlist = Playlist.objects.get(id=playlist_id)
        context['playlist'] = playlist

        # Using the ForeignKey to filter PlaylistItem objects
        context['playlist_items'] = PlaylistItem.objects.filter(
            playlist=playlist
        )
        return context


class PlaylistUpdateView(
        LoginRequiredMixin,
        AuthorRequiredMixin,
        UpdateView
        ):

    model = Playlist
    form_class = PlaylistForm
    template_name = 'user_profile/playlist_update_form.html'

    # Get the playlist items context for the playlist_update_form.html template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlist_items'] = PlaylistItem.objects.filter(
            playlist=self.object
        )
        return context

    # Set the author of the playlist to the current user and validates the form
    def form_valid(self, form):
        # call the handle_form_valid function from utils.py
        return handle_form_valid(
            self, form, "You have successfully saved the changes")

    # Redirect to the playlist_updated page for the updated playlist
    def get_success_url(self):
        # call the get_success_url function from utils.py
        return get_success_url(self, 'playlist_updated')


def add_success_message(request):
    messages.success(request, "You have successfully deleted the playlist!")


class PlaylistDeleteView(
        LoginRequiredMixin,
        AuthorRequiredMixin,
        DeleteView
        ):

    model = Playlist
    template_name = 'user_profile/playlist_delete.html'
    success_url = '/profile/'

    def get_queryset(self):
        return Playlist.objects.filter(author=self.request.user)

    def get_success_url(self):
        # Call the function to add the success message
        add_success_message(self.request)
        return self.success_url
