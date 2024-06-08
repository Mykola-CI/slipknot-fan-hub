from django.test import TestCase
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from user_profile.forms import PlaylistItemForm, PlaylistForm


class PlaylistItemFormTest(TestCase):
    """
    testing PlaylistItemForm
    """

    def setUp(self):
        self.valid_data = {
            'song_title': 'Test Song',
            'artist': 'Test Artist',
            'album': 'Test Album',
            'song_url': 'http://example.com/song',
            'song_comments': 'This is a test comment.',
            'performance_year': 2024,
            'performance_type': 0,
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

    # The names of these methods are descriptive and self-explanatory
    def test_form_valid_with_files(self):
        form_data = self.valid_data.copy()
        form_data.update({
            'song_audio': self.song_audio,
            'song_tabs': self.song_tabs
        })
        form = PlaylistItemForm(
            data=form_data,
            files={'song_audio': self.song_audio, 'song_tabs': self.song_tabs})
        self.assertTrue(form.is_valid())

    def test_form_valid_without_files(self):
        form = PlaylistItemForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_required_fields(self):
        form_data = self.valid_data.copy()
        form_data.pop('song_title')
        form = PlaylistItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('song_title', form.errors)


class PlaylistFormTest(TestCase):
    """
    Testing PlaylistForm
    """

    def setUp(self):
        self.valid_data = {
            'title': 'Test Playlist',
            'description': 'This is a test playlist description.',
            'reference_url': 'http://example.com/playlist',
            'status': 0,  # Draft
        }
        self.featured_image = SimpleUploadedFile(
            name='test_image.jpg',
            # Simulated binary content of a jpeg image
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01',
            content_type='image/jpeg'
        )

    def test_form_valid_without_image(self):
        form = PlaylistForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_required_fields(self):
        form_data = self.valid_data.copy()
        form_data.pop('title')
        form = PlaylistForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    # This patch is needed to avoid a cloudinary error 'Invalid image file'
    @patch('cloudinary.uploader.upload')
    def test_form_valid_with_image(self, mock_upload):
        # Mock return value to include 'public_id' and 'version'
        mock_upload.return_value = {
            'url': 'http://res.cloudinary.com/test_image.jpg',
            'public_id': 'test_image',
            'version': 1234567890
        }
        form_data = self.valid_data.copy()
        form = PlaylistForm(
            data=form_data,
            files={'featured_image': self.featured_image}
        )

        self.assertTrue(form.is_valid())
