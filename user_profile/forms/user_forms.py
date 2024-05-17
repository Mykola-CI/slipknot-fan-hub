from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from user_profile.models import UserProfile
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
