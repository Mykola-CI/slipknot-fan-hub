from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from core.models import PlaylistPost, Comment
from user_profile.models import Playlist, UserProfile, PlaylistItem
from core.forms import CommentForm
from django.utils import timezone


class HomeViewTest(TestCase):
    """
    Testing home  page view
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='password')

        # Create PlaylistPosts and Playlists
        for i in range(13):  # Create 13 posts to test pagination
            playlist = Playlist.objects.create(
                title=f'Playlist {i}',
                description='Content',
                author=self.user,
                created_on=timezone.now()
            )
            PlaylistPost.objects.create(
                playlist=playlist,
                slug=f'playlist-{i}',
                created_on=timezone.now(),
                updated_on=timezone.now()
            )

    def test_home_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/home.html')

    # Test that the home_view returns the correct number of posts - 5 per page
    def test_home_view_pagination(self):
        response = self.client.get(self.url)
        self.assertTrue('playlist_posts' in response.context)
        self.assertEqual(len(response.context['playlist_posts']), 5)

    # Test that the home_view returns the correct number of posts per 2nd page
    def test_home_view_pagination_second_page(self):
        response = self.client.get(self.url, {'page': 2})
        self.assertTrue('playlist_posts' in response.context)
        self.assertEqual(len(response.context['playlist_posts']), 5)

    # Check that the home_view returns the remaining 3 posts per last page
    def test_home_view_pagination_last_page(self):
        response = self.client.get(self.url, {'page': 3})
        self.assertTrue('playlist_posts' in response.context)
        self.assertEqual(len(response.context['playlist_posts']), 3)

    # Should default to last page if page is out of range
    def test_home_view_out_of_range_page(self):
        response = self.client.get(self.url, {'page': 9999})
        self.assertTrue('playlist_posts' in response.context)
        self.assertEqual(len(response.context['playlist_posts']), 3)

    def test_home_view_context_data(self):
        response = self.client.get(self.url)
        self.assertTrue('playlists' in response.context)
        self.assertEqual(len(response.context['playlists']), 13)


class PlaylistPostDetailViewTest(TestCase):
    """
    Testing playlist post detail view
    """

    # Creating a test user, user profile, playlist, playlist post,
    # playlist item, and a comment. Login the user and create the url
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        # Checking if the user_profile exists, if not - create it
        # I am using get_or_create method to avoid IntegrityError
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user, defaults={'about_myself': 'Test bio'})
        self.playlist = Playlist.objects.create(
            title='Test Playlist', author=self.user)
        self.playlist_post = PlaylistPost.objects.create(
            playlist=self.playlist, slug='test-playlist')
        self.playlist_item = PlaylistItem.objects.create(
            playlist=self.playlist, song_title='Test Item')
        self.comment = Comment.objects.create(
            playlist_post=self.playlist_post,
            author=self.user,
            content='Test comment')
        self.url = reverse(
            'playlist_post_detail', kwargs={'slug': self.playlist_post.slug})

    def test_get_context_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/playlist_post_detail.html')

        # Checking if the context data includes the correct objects:
        self.assertEqual(response.context['playlist_post'], self.playlist_post)
        self.assertEqual(response.context['playlist'], self.playlist)
        self.assertEqual(response.context['author_profile'], self.user_profile)
        self.assertQuerysetEqual(
            response.context['playlist_items'],
            PlaylistItem.objects.filter(playlist=self.playlist),
            transform=lambda x: x)
        self.assertQuerysetEqual(
            response.context['comments'],
            Comment.objects.filter(playlist_post=self.playlist_post),
            transform=lambda x: x)
        self.assertEqual(response.context['comment_count'], 1)
        self.assertIsInstance(response.context['comment_form'], CommentForm)

        # I verify that the liked context variable is False.
        self.assertFalse(response.context['liked'])

    def test_post_valid_comment(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'content': 'New test comment'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(content='New test comment').exists())

    def test_post_invalid_comment(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'content': ''  # Invalid because content is required
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/playlist_post_detail.html')
        self.assertFalse(Comment.objects.filter(content='').exists())
        self.assertIsInstance(response.context['comment_form'], CommentForm)
        self.assertTrue(response.context['comment_form'].errors)


class CommentDeleteViewTest(TestCase):
    """
    Testing playlist post detail view
    """

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.other_user = User.objects.create_user(
            username='otheruser', password='12345')

        # Creating a playlist post based on playlist
        self.playlist = Playlist.objects.create(
            title='Test Playlist', author=self.user)
        self.playlist_post = PlaylistPost.objects.create(
            playlist=self.playlist, slug='test-playlist')

        # Create a comment
        self.comment = Comment.objects.create(
            playlist_post=self.playlist_post,
            author=self.user,
            content='Test comment')

    def test_comment_delete_by_author(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('comment_delete',
                    args=[self.playlist_post.slug, self.comment.id]))

        # Check that the comment is deleted
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Comment deleted!')

        # Check redirection
        self.assertRedirects(
            response, reverse(
                'playlist_post_detail', args=[self.playlist_post.slug]))

    def test_comment_delete_by_non_author(self):
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(reverse(
            'comment_delete', args=[self.playlist_post.slug, self.comment.id]))

        # Check that the comment is not deleted
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'You can only delete your own comments!')

        # Check redirection
        self.assertRedirects(
            response, reverse(
                'playlist_post_detail', args=[self.playlist_post.slug]))
