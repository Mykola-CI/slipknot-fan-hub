from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    """
    User Profile model that extends built-in User to add
    about_me, avatar and date of birth fields: one-to-one
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    about_myself = models.TextField(_("about myself"), blank=True)

    # Store avatars in the update UserAdmin model Cloudinary cloud
    avatar = CloudinaryField(
        'image',
        folder='slipknot-fan-avatars',
        blank=True
    )
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user.email})"
