from django import forms
from cloudinary.forms import CloudinaryFileField
from django.core.exceptions import ValidationError
from cloudinary.uploader import upload_resource
from cloudinary.models import CloudinaryResource
from user_profile.models import Playlist, PlaylistItem


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
            'allowed_formats': ['mp3', 'wav']
        },
        autosave=False,
        required=False
    )
    song_tabs = CloudinaryFileField(
        options={
            'resource_type': 'raw',
            'folder': 'fanhub/song_tabs',
            'allowed_formats': ['pdf', 'txt']
        },
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
        self.fields['song_tabs'].label = 'Song tabs, lyrics (pdf or txt only):'
        self.fields['song_audio'].label = 'Song audio (mp3 or wav only):'

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
