from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
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
        try:
            # call the handle_form_valid function from utils.py
            return handle_form_valid(
                self, form, "You have successfully created new playlist!")
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Only image files (jpg, jpeg, png) are allowed.')
        return super().form_invalid(form)

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


class PlaylistManageView(
        LoginRequiredMixin,
        TemplateView):

    template_name = 'user_profile/playlist_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        playlists = Playlist.objects.filter(author=user)

        context['playlists'] = playlists

        return context


class PlaylistUpdateView(
        LoginRequiredMixin,
        AuthorRequiredMixin,
        UpdateView
        ):

    model = Playlist
    form_class = PlaylistForm
    template_name = 'user_profile/playlist_update_form.html'

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Only image files (jpg, jpeg, png) are allowed.')
        return super().form_invalid(form)

    # Get the playlist items context for the playlist_update_form.html template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlist_items'] = PlaylistItem.objects.filter(
            playlist=self.object
        )
        return context

    # Set the author of the playlist to the current user and validates the form
    def form_valid(self, form):
        try:
            # call the handle_form_valid function from utils.py
            return handle_form_valid(
                self, form, "You have successfully saved the changes!")
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

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


def toggle_playlist_status(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)

    # Toggle the status
    if playlist.status == 1:  # If currently "Published"
        playlist.status = 0  # Change to "Draft"
        messages.success(
            request,
            "Your playlist has been successfully removed from the FanHub Blog!"
        )
    else:
        playlist.status = 1  # Change to "Published"
        messages.success(
            request,
            "Your playlist has been successfully shared to the FanHub Blog!"
        )

    playlist.save()

    # Redirect back to the playlist_created page
    return HttpResponseRedirect(reverse('playlist_created', args=[pk]))
