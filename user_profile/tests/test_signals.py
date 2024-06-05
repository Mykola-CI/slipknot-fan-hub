from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile


class UserProfileSignalTests(TestCase):
    """
    Create a new user and check if a UserProfile instance has been created
    """

    def test_user_profile_created(self):
        # Just a new user
        user = User.objects.create_user(username='testuser', password='12345')

        # Checking if the UserProfile instance has been created
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

        # Additionally, making sure the created instance is related to the user
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(user_profile.user, user)
