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
    """
    Form for updating the email of the user profile
    """
    class Meta:
        model = User
        fields = ['email']


class UserPasswordForm(PasswordChangeForm):
    """
    Form for updating the password of the user profile
    """
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class UserNameForm(forms.ModelForm):
    """
    Form for updating the 1st and last names of the user profile
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserDOBForm(forms.ModelForm):
    """
    Form for updating the date of birth of the user profile with widget
    """
    class Meta:
        model = UserProfile
        fields = ['date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class UserAboutForm(forms.ModelForm):
    """
    Form for updating the about myself section of the user profile with
    Summernote widget giving rich text editing capabilities
    """
    class Meta:
        model = UserProfile
        fields = ['about_myself']
        widgets = {
            'about_myself': SummernoteWidget(),
        }


# This custom validator overrides Cloudinary validator to prevent odd messages.
def validate_featured_image_size(value):
    max_size = 10400000  # slightly less than 10MB
    # The function itself is placed in utils.py as serving multiple forms
    validate_file_size(value, max_size)


class UploadAvatarForm(forms.ModelForm):
    """
    Form for updating the avatar image of the user profile
    """

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

    # Override save method to handle the avatar upload and invalid file types
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
