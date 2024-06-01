from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ModeratorSection


@admin.register(ModeratorSection)
class ModeratorSectionAdmin(SummernoteModelAdmin):
    """
    Admin interface for the ModeratorSection model.
    Adds Summernote support to the content and about fields.
    """
    summernote_fields = ('content', 'about')
