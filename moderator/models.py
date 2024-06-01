from django.db import models
from cloudinary.models import CloudinaryField


class ModeratorSection(models.Model):
    """
    Stores content for the moderator section of the website.
    """
    title = models.CharField(max_length=200)
    profile_image = CloudinaryField(
        'image',
        default='placeholder',
        folder='fanhub/moderator',)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    reference_url = models.URLField(blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.title
