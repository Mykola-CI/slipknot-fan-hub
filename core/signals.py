from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from user_profile.models import Playlist
from .models import PlaylistPost

# Dictionary to store the previous status of Playlist instances
previous_status = {}


@receiver(pre_save, sender=Playlist)
def store_previous_status(sender, instance, **kwargs):
    if instance.pk:
        previous_status[instance.pk] = (
            Playlist.objects.get(pk=instance.pk).status)

@receiver(post_save, sender=Playlist)
def create_or_update_or_delete_playlist_post(
        sender, instance, created, **kwargs):
    if created:
        if instance.status == 1:  # 1 corresponds to "Published"
            PlaylistPost.objects.create(playlist=instance)
    else:
        prev_status = previous_status.get(instance.pk)
        if prev_status is not None:
            # From "Published" to "Draft"
            if prev_status == 1 and instance.status == 0:  
                PlaylistPost.objects.filter(playlist=instance).delete()
            # From "Draft" to "Published"
            elif prev_status == 0 and instance.status == 1:
                # Check if a PlaylistPost already exists
                # (might be created through admin console)
                playlist_post, created = PlaylistPost.objects.get_or_create(
                    playlist=instance)
                if not created:
                    # If it already exists, update the updated_on field
                    playlist_post.save()
            elif instance.status == 1:  # Still "Published"
                playlist_post, created = PlaylistPost.objects.get_or_create(
                    playlist=instance)
                if not created:
                    # If it already exists, update the updated_on field
                    playlist_post.save()
        # Clean up the previous status dictionary
        previous_status.pop(instance.pk, None)
