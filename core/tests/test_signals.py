from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models.signals import pre_save, post_save
from user_profile.models import Playlist
from core.models import PlaylistPost
from core.signals import (store_previous_status,
                          create_or_update_or_delete_playlist_post)


class PlaylistSignalTests(TestCase):

    def setUp(self):
        # Connect the signals
        pre_save.connect(store_previous_status, sender=Playlist)
        post_save.connect(
            create_or_update_or_delete_playlist_post, sender=Playlist)
        # Create a user for the author field
        self.user = User.objects.create_user(
            username='daniel', password='121212')

    def tearDown(self):
        # Disconnect the signals
        pre_save.disconnect(store_previous_status, sender=Playlist)
        post_save.disconnect(
            create_or_update_or_delete_playlist_post, sender=Playlist)

    # Test if PlaylistPost instance created when Playlist is set to "Published"
    def test_playlist_post_created_when_published(self):
        playlist = Playlist.objects.create(
            status=1, slug='test-slug', author=self.user)
        self.assertTrue(
            PlaylistPost.objects.filter(playlist=playlist).exists())

    # Test if PlaylistPost instance created and slug set correctly:
    # I simulated the create scenario, the previous_status explicitly defined
    def test_playlist_post_slug_set_correctly(self):
        # Create Playlist instance, no initial status, expected the default '0'
        playlist = Playlist.objects.create(
            slug='slipknot-slug', author=self.user)

        # Manually set the previous_status as required by the signal logic
        previous_status = {}
        previous_status[playlist.pk] = playlist.status

        # Update the Playlist instance to "Published" status
        playlist.status = 1
        playlist.slug = 'slipknot-slug'
        playlist.save()

        # Ensure the PlaylistPost is created
        self.assertTrue(PlaylistPost.objects.filter(playlist=playlist).exists())

        playlist_post = PlaylistPost.objects.get(playlist=playlist)

        # Assert that the slug is set correctly
        self.assertEqual(playlist_post.slug, 'slipknot-slug')

    # Test if PlaylistPost instance deleted when Playlist is set to "Draft"
    def test_playlist_post_deleted_when_draft(self):
        playlist = Playlist.objects.create(
            status=1, slug='test-slug', author=self.user)
        playlist.status = 0
        playlist.save()
        self.assertFalse(
            PlaylistPost.objects.filter(playlist=playlist).exists())

    # Test if PlaylistPost instance slug updated when Playlist slug updated
    def test_playlist_post_slug_updated(self):
        playlist = Playlist.objects.create(
            status=1, slug='initial-slug', author=self.user)
        playlist.slug = 'updated-slug'
        playlist.save()
        playlist_post = PlaylistPost.objects.get(playlist=playlist)
        self.assertEqual(playlist_post.slug, 'updated-slug')

    def test_playlist_post_created_when_published_from_draft(self):
        playlist = Playlist.objects.create(
            status=0, slug='test-slug', author=self.user)
        playlist.status = 1
        playlist.save()
        self.assertTrue(
            PlaylistPost.objects.filter(playlist=playlist).exists())
