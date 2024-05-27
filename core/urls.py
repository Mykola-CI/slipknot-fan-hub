from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path(
        'playlistpost/<int:pk>/',
        views.PlaylistPostDetailView.as_view(),
        name='playlist_post_detail'),
]
