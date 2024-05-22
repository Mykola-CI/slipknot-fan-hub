from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)
from ..forms.playlist_forms import PlaylistItemForm
from ..models import Playlist, PlaylistItem
from ..utils import AuthorRequiredMixin


class PlaylistItemCreateView(LoginRequiredMixin, CreateView):
    model = PlaylistItem
    form_class = PlaylistItemForm
    template_name = 'user_profile/add_playlist_item.html'

    def form_valid(self, form):
        # Set the playlist attribute from the URL
        form.instance.playlist = Playlist.objects.get(
            pk=self.kwargs['playlist_id'])
        response = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully added song to your playlist!",
        )
        return response

    def get_success_url(self):
        # Redirect to the 'playlist_created' page for the specific playlist
        return reverse_lazy(
            'playlist_created', kwargs={'pk': self.object.playlist.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the playlist to the context
        context['playlist'] = Playlist.objects.get(
            pk=self.kwargs['playlist_id'])
        return context


class PlaylistItemUpdateView(
        LoginRequiredMixin,
        AuthorRequiredMixin,
        UpdateView):
    model = PlaylistItem
    form_class = PlaylistItemForm
    template_name = 'user_profile/playlist_item_update.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            "You have successfully saved changes to your playlist item!",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'playlist_updated', kwargs={'pk': self.object.playlist.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the playlist to the context
        context['playlist'] = get_object_or_404(
            Playlist, id=self.kwargs['playlist_id'])
        context['item'] = get_object_or_404(
            PlaylistItem, id=self.kwargs['pk'])

        return context


class PlaylistItemDeleteView(
        LoginRequiredMixin,
        AuthorRequiredMixin,
        DeleteView):
    model = PlaylistItem
    template_name = 'user_profile/delete_playlist_item.html'

    def get_success_url(self):
        messages.success(
            self.request, "You have successfully deleted the playlist item.")
        # Redirect to the 'playlist_created' page for the specific playlist
        return reverse_lazy(
            'playlist_created', kwargs={'pk': self.object.playlist.pk}
        )
