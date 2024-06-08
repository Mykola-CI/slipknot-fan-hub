from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from user_profile.forms import PlaylistItemForm


class PlaylistItemFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'song_title': 'Test Song',
            'artist': 'Test Artist',
            'album': 'Test Album',
            'song_url': 'http://example.com/song',
            'song_comments': 'This is a test comment.',
            'performance_year': 2024,
            'performance_type': 'Original',
        }
        self.song_audio = SimpleUploadedFile(
            name='test_audio.mp3',
            content=b'This is a test audio file.',
            content_type='audio/mpeg'
        )
        self.song_tabs = SimpleUploadedFile(
            name='test_tabs.pdf',
            content=b'This is a test tabs file.',
            content_type='application/pdf'
        )

    # @patch('cloudinary.uploader.upload')
    # def test_form_valid_with_files(self, mock_upload):
    #     mock_upload.return_value = {
    #         'url': 'http://res.cloudinary.com/test_audio.mp3',
    #         'public_id': 'test_audio',
    #         'version': 1234567890
    #     }
    #     form_data = self.valid_data.copy()
    #     form = PlaylistItemForm(data=form_data, files={'song_audio': self.song_audio, 'song_tabs': self.song_tabs})

    #     # Print form errors for debugging
    #     if not form.is_valid():
    #         print("Form errors:", form.errors)

    #     self.assertTrue(form.is_valid())

    def test_form_valid_without_files(self):
        form = PlaylistItemForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_required_fields(self):
        form_data = self.valid_data.copy()
        form_data.pop('song_title')
        form = PlaylistItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('song_title', form.errors)
