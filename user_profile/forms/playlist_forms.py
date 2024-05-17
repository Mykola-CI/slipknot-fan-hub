from django import forms
from user_profile.models import Playlist, PlaylistItem
from cloudinary.forms import CloudinaryFileField


class PlaylistForm(forms.ModelForm):
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


class PlaylistItemForm(forms.ModelForm):
    song_video = CloudinaryFileField(
        options={
            'folder': 'fanhub/song_videos'
        },
        required=False
    )
    song_audio = CloudinaryFileField(
        options={
                'folder': 'fanhub/song_audios'
        },
        required=False
    )
    song_tabs = CloudinaryFileField(
        options={
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
            'song_video',
            'song_audio',
            'song_tabs',
            'song_comments',
            'performance_year',
            'performance_type'
        ]
