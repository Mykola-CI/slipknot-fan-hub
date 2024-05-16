from django.shortcuts import render


# Handle 403 Forbidden error in separate page
def my_custom_permission_denied_view(request, exception):
    context = {'exception': str(exception)}
    return render(request, 'user_profile/403.html', context, status=403)
