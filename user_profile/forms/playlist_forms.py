from django import forms
from user_profile.models import Playlist, PlaylistItem
from cloudinary.forms import CloudinaryFileField


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
            }
        },
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


class PlaylistItemForm(forms.ModelForm):
    """
    Form for creating and updating Playlist Items
    """
    song_audio = CloudinaryFileField(
        options={
            'resource_type': 'raw',
            'folder': 'fanhub/song_audios'
        },
        required=False
    )
    song_tabs = CloudinaryFileField(
        options={
            'resource_type': 'raw',
            'folder': 'fanhub/song_tabs'
        },
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
        self.fields['song_tabs'].label = 'Song tabs, lyrics (pdf or txt only):'
        self.fields['song_audio'].label = 'Song audio (mp3 or wav only):'
