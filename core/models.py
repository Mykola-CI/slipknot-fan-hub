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
    slug = models.SlugField(unique=True, null=False)
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
    content = models.CharField(max_length=500)
    likes_comment = models.ManyToManyField(
        User, related_name="playlist_comments", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def total_likes_comment(self):
        return self.likes_comment.count()

    # Check if the current user has liked the comment (False or True)
    # GETTER method decorator and definition:
    @property
    def is_liked_by_user(self):
        return self._is_liked_by_user

    # SETTER method decorator and definition:
    @is_liked_by_user.setter
    def is_liked_by_user(self, user):
        # prefix '_' to indicate that this is a private attribute
        self._is_liked_by_user = self.likes_comment.filter(id=user.id).exists()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.content} by {self.author}"
