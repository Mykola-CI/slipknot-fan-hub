from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile, Playlist, PlaylistItem
from cloudinary.forms import CloudinaryFileField


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class UserPasswordForm(PasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserDOBForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class UserAboutForm(forms.ModelForm):
    about_myself = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 'auto',
            'class': 'input-padding'
            }),
        label='Add a few words, express yourself...',
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['about_myself']


class UploadAvatarForm(forms.ModelForm):
    avatar = CloudinaryFileField()

    class Meta:
        model = UserProfile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].options = {
            'folder': 'fan-avatar-thumbs',
            'format': 'png',
            'transformation': {
                'width': 300,
                'height': 300,
                'crop': 'thumb',
                'gravity': 'face',
                'radius': 'max',
                'zoom': 0.70,
                'background': 'transparent'
            }
        }


class PlaylistForm(forms.ModelForm):
    featured_image = CloudinaryFileField(
        options={
            'crop': 'limit',
            'width': 600,
            'height': 600,
        }
    )

    class Meta:
        model = Playlist
        fields = [
            'title',
            'slug',
            'featured_image',
            'description',
            'reference_url',
            'status'
        ]


class PlaylistItemForm(forms.ModelForm):
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
