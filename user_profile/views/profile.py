from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from ..forms.user_forms import (
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

    # Handling AJAX requests for loading formsI wonder why whenever I save 
    if (request.method == 'GET' and
            request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        form_type = request.GET.get('form_type', '')
        form = None
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
        if form is not None:
            return HttpResponse(form.as_p())
    # If form is None, just return an empty response to avoid error
        return HttpResponse("")


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
            try:
                form.save()
                return JsonResponse({'status': 'success'})
            except ValidationError as e:
                error_message = str(e).strip('[]').replace('"', '')
                return JsonResponse(
                    {'status': 'error', 'errors': error_message})

        else:
            # Extract and format errors into a single string
            # this is to ensure that errors are in readable format
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)
            error_message = " ".join(errors)
            return JsonResponse(
                {'status': 'error', 'errors': error_message})

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
