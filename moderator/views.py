from django.shortcuts import render
from .models import ModeratorSection


def moderator_section_view(request):
    """
    Renders moderator content, such as
    news and updates, to the user.
    """

    moderator = ModeratorSection.objects.all().order_by('-updated_on').first()

    return render(
        request,
        "moderator/moderator-section.html",
        {"moderator": moderator},
    )
