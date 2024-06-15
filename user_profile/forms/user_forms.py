from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from user_profile.models import UserProfile
from cloudinary.forms import CloudinaryFileField
from cloudinary.uploader import upload_resource
from cloudinary.models import CloudinaryResource
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget


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
    class Meta:
        model = UserProfile
        fields = ['about_myself']
        widgets = {
            'about_myself': SummernoteWidget(),
        }


class UploadAvatarForm(forms.ModelForm):
    avatar = CloudinaryFileField(autosave=False)

    class Meta:
        model = UserProfile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].options = {
            'folder': 'fan-avatar-thumbs',
            'format': 'png',
            'allowed_formats': ['jpg', 'jpeg', 'png', 'webp'],
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

    def save(self, commit=True):
        instance = super(UploadAvatarForm, self).save(commit=False)
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if isinstance(avatar, CloudinaryResource):
                instance.avatar = avatar
            else:
                try:
                    instance.avatar = upload_resource(
                        avatar,
                        **self.fields['avatar'].options)
                except Exception as e:
                    raise ValidationError(
                        f"{e} | try allowed formats: jpg, jpeg, png or webp")

        if commit:
            instance.save()
        return instance
