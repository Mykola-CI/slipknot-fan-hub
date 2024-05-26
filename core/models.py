from django.db import models
from django.contrib.auth.models import User
from user_profile.models import Playlist


class PlaylistPost(models.Model):
    """
    Stores user playlist publication instances
    """

    playlist = models.OneToOneField(
        Playlist, on_delete=models.CASCADE, related_name="playlist_post"
    )
    likes = models.ManyToManyField(
        User, related_name="playlist_likes", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.playlist.title} | by {self.playlist.author.username}"


class Comment(models.Model):
    """
    Stores a single comment entry related to User and to PlaylistPost.
    """
    playlist_post = models.ForeignKey(PlaylistPost, on_delete=models.CASCADE,
                                      related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField()
    likes = models.ManyToManyField(
        User, related_name="playlist_comments", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
