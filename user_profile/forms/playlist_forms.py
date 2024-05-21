from django import forms
from django_summernote.widgets import SummernoteWidget
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
        widgets = {
            'description': SummernoteWidget(),
        }


class PlaylistItemForm(forms.ModelForm):
    song_video = CloudinaryFileField(
        options={
            'resource_type': 'video',
            'folder': 'fanhub/song_videos'
        },
        required=False
    )
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
            'song_video',
            'song_audio',
            'song_tabs',
            'song_comments',
            'performance_year',
            'performance_type'
        ]
