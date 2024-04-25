from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # triggers when user created

    else:  # triggers when a user updates User model data
        # Check if the user has a related UserProfile instance to avoid error
        if hasattr(instance, 'profile'):
            instance.profile.save()
