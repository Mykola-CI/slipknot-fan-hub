from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms import (
    UserEmailForm,
    UserPasswordForm,
    UserNameForm,
    UserDOBForm,
    UserAboutForm,
    UploadAvatarForm
)
from ..models import UserProfile, Playlist


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
