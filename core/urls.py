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
    path(
        'playlistpost/<int:pk>/likes', views.like_view, name='like_view'),
    path(
        'playlistpost/<int:pk>/comment/<int:comment_id>/like/',
        views.like_comment,
        name='like_comment'
    ),
    path(
        'playlistpost/list/',
        views.PlaylistPreviewView.as_view(),
        name='playlist_list'),
]
