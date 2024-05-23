from django.views import generic
from .models import PlaylistPost


class HomeView(generic.ListView):
    template_name = 'core/home.html'
    queryset = PlaylistPost.objects.all().order_by('-created_on')
    paginate_by = 6

    # Making available the user object to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
