from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path(
        'playlistpost/list/',
        views.PlaylistPreviewView.as_view(),
        name='playlist_list'),
    path(
        'playlistpost/<slug:slug>/',
        views.PlaylistPostDetailView.as_view(),
        name='playlist_post_detail'),
    path(
        'playlistpost/<slug:slug>/edit_comment/<int:comment_id>',
        views.comment_edit, name='comment_edit'),
    path(
        'playlistpost/<slug:slug>/delete_comment/<int:comment_id>',
        views.comment_delete, name='comment_delete'),
    path(
        'playlistpost/<slug:slug>/likes', views.like_view, name='like_view'),
    path(
        'playlistpost/<slug:slug>/comment/<int:comment_id>/like/',
        views.like_comment,
        name='like_comment'
    ),
    path(
        'presentation/<str:username>/',
        views.user_profile_presentation,
        name='user_profile_presentation'),
]
