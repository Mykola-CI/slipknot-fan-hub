from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator


class UserProfile(models.Model):
    """
    User Profile model that extends built-in User to add
    about_myself, avatar and date of birth fields: one-to-one
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    about_myself = models.TextField(
        _("about myself"),
        blank=True,
        # Limit characters to 500 as max_length does not apply to TextField
        validators=[MaxLengthValidator(500)]
    )

    # Store avatars in the update UserAdmin model Cloudinary cloud
    avatar = CloudinaryField(
        'image',
        default='default_avatar',
        folder='slipknot-fan-avatars',
        blank=True
    )
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user.email})"


STATUS = ((0, "Draft"), (1, "Published"))
TYPE = ((0, "Original"), (1, "Cover"), (2, "Tutorial"), (3, "Inspired"))


class Playlist(models.Model):
    """
    Stores user playlist general info and umbrella image
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playlists"
    )
    featured_image = CloudinaryField(
        'image',
        folder='fanhub/playlist_images',
        blank=True)
    description = models.TextField(
        blank=True,
        # Limit characters to 500 as max_length does not apply to TextField
        validators=[MaxLengthValidator(500)])
    reference_url = models.URLField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def is_author(self, user):
        return self.author == user

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance already exists
            original = Playlist.objects.get(pk=self.pk)
            if original.title != self.title:  # Check if the title has changed
                self.slug = slugify(self.title)
                # Ensure the slug is unique
                original_slug = self.slug
                num = 1
                while Playlist.objects.filter(slug=self.slug).exists():
                    self.slug = f'{original_slug}-{num}'
                    num += 1
        else:
            self.slug = slugify(self.title)
            # Ensure the slug is unique
            original_slug = self.slug
            num = 1
            while Playlist.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1

        super(Playlist, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | status: {self.get_status_display()}"


class PlaylistItem(models.Model):
    """
    Stores playlist items
    """
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, related_name="playlist_items"
    )
    song_title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    song_url = models.URLField(blank=True)
    song_audio = CloudinaryField(
        'audios',
        resource_type='raw',
        folder='fanhub/song_audios',
        blank=True)
    song_tabs = CloudinaryField(
        'docs',
        resource_type='raw',
        folder='fanhub/song_tabs',
        blank=True)
    song_comments = models.TextField(
        blank=True,
        # Limit characters to 500 as max_length does not apply to TextField
        validators=[MaxLengthValidator(500)])
    performance_year = models.IntegerField(
        verbose_name="Year of Performance", blank=True, null=True)
    performance_type = models.IntegerField(choices=TYPE, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"'{self.song_title}' by {self.artist} | "
        )
