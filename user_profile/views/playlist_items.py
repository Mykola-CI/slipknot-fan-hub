from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView
)
from ..forms.playlist_forms import PlaylistItemForm
from ..models import Playlist, PlaylistItem


class PlaylistItemCreateView(LoginRequiredMixin, CreateView):
    model = PlaylistItem
    form_class = PlaylistItemForm
    template_name = 'user_profile/add_playlist_item.html'

    def form_valid(self, form):
        # Set the playlist attribute from the URL
        form.instance.playlist = Playlist.objects.get(
            pk=self.kwargs['playlist_id'])
        response = super(self.__class__, self).form_valid(form)
        messages.success(
            self.request,
            "You have successfully added song to your playlist",
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
