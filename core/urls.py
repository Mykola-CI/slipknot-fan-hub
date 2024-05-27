from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path(
        'playlistpost/<int:pk>/',
        views.PlaylistPostDetailView.as_view(),
        name='playlist_post_detail'),
    path(
        'playlistpost/<int:pk>/edit_comment/<int:comment_id>',
        views.comment_edit, name='comment_edit'),
    path(
        'playlistpost/<int:pk>/delete_comment/<int:comment_id>',
        views.comment_delete, name='comment_delete'),
]
