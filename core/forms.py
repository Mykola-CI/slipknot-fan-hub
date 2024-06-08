from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    ModelForm class for users to create comment on a playlist_post
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Comment
        fields = ('content',)
