from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from user_profile.views import PlaylistCreatedView
from user_profile.models import Playlist, PlaylistItem


class PlaylistCreatedViewTest(TestCase):
    """
    Testing selected functionality points of the PlaylistCreatedView view
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
            username='user1', password='password1')
        self.user2 = User.objects.create_user(
            username='user2', password='password2')
        self.playlist = Playlist.objects.create(
            title='Test Playlist', author=self.user1)
        self.playlist_item = PlaylistItem.objects.create(
            playlist=self.playlist, song_title='Test Item')

    # In fact, it is more testing the AuthorRequiredMixin and how it works
    # in conjunction with the PlaylistCreatedView
    def test_unauthorized_user_access(self):
        request = self.factory.get(
            reverse('playlist_created', kwargs={'pk': self.playlist.pk}))
        request.user = self.user2

        with self.assertRaises(PermissionDenied):
            PlaylistCreatedView.as_view()(request, pk=self.playlist.pk)

    # Simply checking if the context data is correctly passed to the template
    def test_context_data(self):
        request = self.factory.get(
            reverse('playlist_created', kwargs={'pk': self.playlist.pk}))
        request.user = self.user1
        response = PlaylistCreatedView.as_view()(request, pk=self.playlist.pk)
        context = response.context_data
        self.assertEqual(context['playlist'], self.playlist)
        self.assertIn(self.playlist_item, context['playlist_items'])

    # Testing the case when the playlist does not exist
    def test_non_existent_playlist(self):
        request = self.factory.get(
            reverse('playlist_created', kwargs={'pk': 999}))
        request.user = self.user1
        with self.assertRaises(Http404):
            PlaylistCreatedView.as_view()(request, pk=999)


class PlaylistUpdateViewTests(TestCase):
    """
    Testing selected functionality points of the PlaylistUpdateView view
    """
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.other_user = User.objects.create_user(
            username='otheruser', password='password')

        # Create a playlist
        self.playlist = Playlist.objects.create(
            title='Test Playlist', author=self.user)

        # Create playlist items
        self.playlist_item = PlaylistItem.objects.create(
            playlist=self.playlist, song_title='Test Item')

        # URL for the update view
        self.url = reverse('playlist_update', kwargs={'pk': self.playlist.pk})

    # Check if accessed by a logged-in user
    def test_logged_in_user_can_access_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'user_profile/playlist_update_form.html')

    # Check if NOT accessed by a non-logged-in user
    def test_non_logged_in_user_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    # Check if NOT accessed by a logged-in but not an author user
    def test_non_author_user_cannot_access_update_view(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    # Check if the context data is correctly passed to the template
    def test_context_contains_playlist_items(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('playlist_items', response.context)
        self.assertQuerysetEqual(
            response.context['playlist_items'],
            PlaylistItem.objects.filter(playlist=self.playlist)
        )

    # Test that a valid form submission updates the playlist
    def test_valid_form_submission_updates_playlist(self):
        self.client.login(username='testuser', password='password')
        data = {
            'title': 'Updated Playlist Name',
            'description': 'Updated Playlist Description',
            'reference_url': 'https://updated-reference-url.com',
            'status': 1
        }
        response = self.client.post(self.url, data)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.title, 'Updated Playlist Name')
        self.assertEqual(
            self.playlist.description, 'Updated Playlist Description')
        self.assertEqual(
            self.playlist.reference_url, 'https://updated-reference-url.com')
        self.assertEqual(self.playlist.status, 1)
        self.assertRedirects(
            response,
            reverse('playlist_updated', kwargs={'pk': self.playlist.pk}))


class PlaylistDeleteViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.playlist = Playlist.objects.create(
            author=self.user, title='Test Playlist')
        self.url = reverse('playlist_delete', args=[self.playlist.id])

    # Ensure that only authenticated users can access the view.
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/playlist_delete.html')

    # Testing deletion of a playlist
    def test_playlist_deletion(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url)
        self.assertRedirects(response, '/profile/')
        self.assertFalse(Playlist.objects.filter(id=self.playlist.id).exists())
