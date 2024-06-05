from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from ..models import UserProfile, Playlist
import os


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='mock@example.com', password='12345')
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user)
        self.client.login(username='testuser', password='12345')

    # I am checking the presence of the mock email address and the label title
    # in the response content
    def test_get_email_form(self):
        response = self.client.get(
            reverse('profile'), {'form_type': 'email'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mock@example.com')
        self.assertContains(response, 'Email address:')

    # Checking form submitted with valid email address
    def test_post_email_form_valid(self):
        response = self.client.post(reverse('profile'), {
            'form_type': 'email',
            'email': 'newemail@example.com'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

    # Checking form submitted with invalid email address to return error status
    def test_post_email_form_invalid(self):
        response = self.client.post(reverse('profile'), {
            'form_type': 'email',
            'email': 'invalid-email'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertContains(response, '"status": "error"')
        self.assertContains(
            response, 'Enter a valid email address.')

    # Checking form submit for first and last name
    def test_post_name_form_valid(self):
        response = self.client.post(reverse('profile'), {
            'form_type': 'name',
            'first_name': 'NewName',
            'last_name': 'NewLastName'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

    # Checking form submit for date of birth
    def test_post_dob_form_valid(self):
        response = self.client.post(reverse('profile'), {
            'form_type': 'dob',
            'date_of_birth': '2000-01-01'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

    # Checking form submit for about section
    def test_post_about_form_valid(self):
        response = self.client.post(reverse('profile'), {
            'form_type': 'about',
            'about_myself': 'This is a test about section.'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

    # Checking form submit for avatar upload
    def test_post_avatar_form_valid(self):
        avatar_path = os.path.join(
            settings.BASE_DIR, 'static', 'images', 'nobody.jpg')
        with open(avatar_path, 'rb') as avatar:
            response = self.client.post(reverse('profile'), {
                'form_type': 'avatar',
                'avatar': avatar
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

    # Testing the profile view for an unauthenticated user.
    # I tried to simulate logging out and then accessing the profile page.
    # Expectation is a redirect to the login page and after that to 'profile'.
    def test_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/accounts/login/?next={reverse('profile')}")

    # Testing the profile view for an authenticated user.
    # I am checking the response status code and the title of the page.
    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<title>Slipknot Fan Profile</title>', html=True)


class ProfileViewContextTests(TestCase):
    """
    Here I check if contexts of the profile view are rendered correctly.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')

        # No need to manually create UserProfile, it is created by the signal
        self.user_profile = UserProfile.objects.get(user=self.user)

        self.playlist = Playlist.objects.create(
            author=self.user, title='Test Playlist', slug='test-playlist')
        self.client.login(username='testuser', password='12345')

    def test_profile_context(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/profile.html')
        self.assertIn('user_profile', response.context)
        self.assertIn('playlists', response.context)
        self.assertIn('email_form', response.context)
        self.assertIn('password_form', response.context)
        self.assertIn('name_form', response.context)
        self.assertIn('dob_form', response.context)
        self.assertIn('about_form', response.context)
        self.assertIn('avatar_form', response.context)

        # This is to make sure that a mock playlist exists in context
        self.assertEqual(len(response.context['playlists']), 1)
        self.assertEqual(response.context['playlists'][0], self.playlist)
