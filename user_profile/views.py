from django.shortcuts import render
from .models import UserProfile


def user_profile_view(request):
    return render(request, 'user_profile/user-profile.html')
