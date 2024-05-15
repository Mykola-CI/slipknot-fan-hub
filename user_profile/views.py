from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, UpdateView
from .forms import (
    UserEmailForm,
    UserPasswordForm,
    UserNameForm,
    UserDOBForm,
    UserAboutForm,
    UploadAvatarForm,
    PlaylistForm
)
from .models import UserProfile, Playlist, PlaylistItem
from .utils import handle_form_valid, get_success_url, AuthorRequiredMixin


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    playlists = Playlist.objects.filter(author=request.user)

    # Handling AJAX requests for loading forms
    if (request.method == 'GET' and
            request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        form_type = request.GET.get('form_type', '')
        if form_type == 'email':
            form = UserEmailForm(instance=request.user)
        elif form_type == 'password':
            form = UserPasswordForm(request.user)
        elif form_type == 'name':
            form = UserNameForm(instance=request.user)
        elif form_type == 'dob':
            form = UserDOBForm(instance=user_profile)
        elif form_type == 'about':
            form = UserAboutForm(instance=user_profile)
        elif form_type == 'avatar':
            form = UploadAvatarForm(instance=user_profile)
        return HttpResponse(form.as_p())

    # Handling AJAX requests for form submission
    if (request.method == 'POST' and
            request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        form_type = request.POST.get('form_type')

        if form_type == 'email':
            form = UserEmailForm(request.POST, instance=request.user)
        elif form_type == 'password':
            form = UserPasswordForm(request.user, request.POST)
        elif form_type == 'name':
            form = UserNameForm(request.POST, instance=request.user)
        elif form_type == 'dob':
            form = UserDOBForm(request.POST, instance=user_profile)
        elif form_type == 'about':
            form = UserAboutForm(request.POST, instance=user_profile)
        elif form_type == 'avatar':
            form = UploadAvatarForm(
                request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        elif form:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors.as_json()})
        else:
            return JsonResponse(
                {'status': 'error', 'errors': form.errors.as_json()})

    # Context for initial page load
    context = {
        'user_profile': user_profile,
        'playlists': playlists,
        'email_form': UserEmailForm(instance=request.user),
        'password_form': UserPasswordForm(request.user),
        'name_form': UserNameForm(instance=request.user),
        'dob_form': UserDOBForm(instance=user_profile),
        'about_form': UserAboutForm(instance=user_profile),
        'avatar_form': UploadAvatarForm(instance=user_profile),
    }
    return render(request, 'user_profile/profile.html', context)


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'user_profile/playlist_form.html'

    # Set the author of the playlist to the current user and validates the form
    def form_valid(self, form):
        # call the handle_form_valid function from utils.py
        return handle_form_valid(self, form)

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
        playlist_id = self.kwargs.get('pk')
        context['playlist'] = Playlist.objects.get(id=playlist_id)
        return context


class PlaylistUpdateView(
        LoginRequiredMixin,
        UpdateView,
        AuthorRequiredMixin):

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
        return handle_form_valid(self, form)

    # Redirect to the playlist_updated page for the updated playlist
    def get_success_url(self):
        # call the get_success_url function from utils.py
        return get_success_url(self, 'playlist_updated')


# Handle 403 Forbidden error in separate page
def my_custom_permission_denied_view(request, exception):
    context = {'exception': str(exception)}
    return render(request, 'user_profile/403.html', context, status=403)
