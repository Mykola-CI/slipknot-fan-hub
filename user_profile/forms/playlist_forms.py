from django import forms
from cloudinary.forms import CloudinaryFileField
from django.core.exceptions import ValidationError
from cloudinary.uploader import upload_resource
from cloudinary.models import CloudinaryResource
from user_profile.models import Playlist, PlaylistItem
from user_profile.utils import validate_file_size


# This custom validator overrides Cloudinary validator and
# prevents from forced embarrassing messages.
def validate_featured_image_size(value):
    max_size = 10400000  # slightly less than 10MB
    validate_file_size(value, max_size)


def validate_song_audio_size(value):
    max_size = 8388608  # 8MB
    validate_file_size(value, max_size)


def validate_song_tabs_size(value):
    max_size = 5242880  # 5MB
    validate_file_size(value, max_size)


class PlaylistForm(forms.ModelForm):
    """
    Form for creating and updating Playlist model instances
    """

    featured_image = CloudinaryFileField(
        options={
            'folder': 'fanhub/playlist_images',
            'transformation': {
                'crop': 'limit',
                'width': 600,
                'height': 600
            },
            'allowed_formats': ['jpg', 'jpeg', 'png', 'webp']
        },
        # Call custom validator to prevent from forced messages from Cloudinary
        validators=[validate_featured_image_size],
        autosave=False,
        required=False
    )

    class Meta:
        model = Playlist
        fields = [
            'title',
            'featured_image',
            'description',
            'reference_url',
            'status'
        ]
        labels = {
            'title': 'Playlist Title*:'
        }

    # Override the __init__ method to set custom labels for Cloudinary fields
    def __init__(self, *args, **kwargs):
        super(PlaylistForm, self).__init__(*args, **kwargs)
        self.fields['featured_image'].label = (
            'Choose Banner (jpg, webp, png, 10MB max):')

    # Override save method to handle banner image upload and invalid file types
    def save(self, commit=True):
        instance = super(PlaylistForm, self).save(commit=False)
        featured_image = self.cleaned_data.get('featured_image')

        if featured_image:
            if isinstance(featured_image, CloudinaryResource):
                instance.featured_image = featured_image
            else:
                try:
                    instance.featured_image = upload_resource(
                        featured_image,
                        **self.fields['featured_image'].options)
                except Exception as e:
                    raise ValidationError(
                        f"Error uploading featured image: {e}")

        if commit:
            instance.save()
        return instance


class PlaylistItemForm(forms.ModelForm):
    """
    Form for creating and updating Playlist Items
    """
    song_audio = CloudinaryFileField(
        options={
            'resource_type': 'raw',
            'folder': 'fanhub/song_audios',
            'allowed_formats': ['mp3', 'wav', 'aac']
        },
        # Call custom validator to restrict the file size
        validators=[validate_song_audio_size],
        autosave=False,
        required=False
    )
    song_tabs = CloudinaryFileField(
        options={
            'resource_type': 'raw',
            'folder': 'fanhub/song_tabs',
            'allowed_formats': ['pdf', 'txt']
        },
        # Call custom validator to restrict the file size
        validators=[validate_song_tabs_size],
        autosave=False,
        required=False
    )

    class Meta:
        model = PlaylistItem
        fields = [
            'song_title',
            'artist',
            'album',
            'song_url',
            'song_audio',
            'song_tabs',
            'song_comments',
            'performance_year',
            'performance_type'
        ]
        labels = {
            'song_title': 'Song Title*:',
            'artist': 'Artist*:'
        }

    # Override the __init__ method to set custom labels for Cloudinary fields
    def __init__(self, *args, **kwargs):
        super(PlaylistItemForm, self).__init__(*args, **kwargs)
        self.fields['song_tabs'].label = (
            'Song info (pdf or txt files only, 5MB max):')
        self.fields['song_audio'].label = (
            'Audio file (mp3, wav, aac only, 8MB max):')

    def save(self, commit=True):
        instance = super(PlaylistItemForm, self).save(commit=False)
        song_audio = self.cleaned_data.get('song_audio')
        song_tabs = self.cleaned_data.get('song_tabs')

        if song_audio:
            if isinstance(song_audio, CloudinaryResource):
                instance.song_audio = song_audio
            else:
                try:
                    instance.song_audio = upload_resource(
                        song_audio, **self.fields['song_audio'].options)
                except Exception as e:
                    raise ValidationError(f"Error uploading song audio: {e}")

        if song_tabs:
            if isinstance(song_tabs, CloudinaryResource):
                instance.song_tabs = song_tabs
            else:
                try:
                    instance.song_tabs = upload_resource(
                        song_tabs, **self.fields['song_tabs'].options)
                except Exception as e:
                    raise ValidationError(f"Error uploading song tabs: {e}")

        if commit:
            instance.save()
        return instance
