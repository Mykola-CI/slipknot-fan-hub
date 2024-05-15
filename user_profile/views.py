from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
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
from .models import UserProfile, Playlist


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

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"You have successfully created {form.instance.title} playlist")
        return response

    def get_success_url(self):
        # Redirect to the Playlist item create page for the new playlist
        return reverse(
            'playlist_created',
            kwargs={'playlist_id': self.object.id}
        )


class PlaylistCreatedView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile/playlist_created.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist_id = self.kwargs.get('playlist_id')
        context['playlist'] = Playlist.objects.get(id=playlist_id)
        return context

    # Check if the user is the author of the playlist (override 'get' method)
    def get(self, request, *args, **kwargs):
        playlist_id = kwargs['playlist_id']
        playlist = get_object_or_404(Playlist, pk=playlist_id)

        if not playlist.is_author(request.user):
            raise PermissionDenied(
                "You are not authorised to access this page"
            )

        return super().get(request, *args, **kwargs)


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'user_profile/playlist_update_form.html'
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"You have successfully created '{form.instance.title}' playlist")
        return response

    def get_success_url(self):
        return reverse(
            'playlist_updated',
            kwargs={'playlist_id': self.object.id}
        )

    # Check if the user is the author of the playlist (override 'get' method)
    # Here 'pk' is passed as a keyword argument to the URL
    def get(self, request, *args, **kwargs):
        playlist_id = kwargs['pk']
        playlist = get_object_or_404(Playlist, pk=playlist_id)

        if not playlist.is_author(request.user):
            raise PermissionDenied(
                "You are not authorised to access this page"
            )

        return super().get(request, *args, **kwargs)


# Handle 403 Forbidden error in separate page
def my_custom_permission_denied_view(request, exception):
    context = {'exception': str(exception)}
    return render(request, 'user_profile/403.html', context, status=403)
