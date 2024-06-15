from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from user_profile.models import UserProfile
from cloudinary.forms import CloudinaryFileField
from cloudinary.uploader import upload_resource
from cloudinary.models import CloudinaryResource
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget
from user_profile.utils import validate_file_size


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


# When file size exceeds 10MB Cloudinary validator forces its messages
# before the file is cropped and resized by widgets. The maximum size of the
# image is cropped afterwords anyway to 600 x 600 and hardly can reach 2MB.
# This custom validator overrides Cloudinary to prevent odd messages.
def validate_featured_image_size(value):
    max_size = 10400000  # slightly less than 10MB
    validate_file_size(value, max_size)


class UploadAvatarForm(forms.ModelForm):
    avatar = CloudinaryFileField(
        autosave=False,
        validators=[validate_featured_image_size],
        required=False
    )

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
                        f"{e} | try allowed formats: jpg, png or webp")

        if commit:
            instance.save()
        return instance
