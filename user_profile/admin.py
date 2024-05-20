from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Playlist, PlaylistItem
from django_summernote.admin import (
    SummernoteModelAdmin,
    SummernoteInlineModelAdmin
)


class UserProfileInline(SummernoteInlineModelAdmin, admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    summernote_fields = ('about_myself',)


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active', 'get_about_myself', 'get_avatar')
    search_fields = ('username', 'first_name', 'last_name', 'email',
                     'profile__about_myself')

    def get_about_myself(self, obj):
        # Check if User Profile is available
        if hasattr(obj, 'profile'):
            return obj.profile.about_myself
        return _("No profile available")

    def get_avatar(self, obj):
        if hasattr(obj, 'profile') and obj.profile.avatar:
            return obj.profile.avatar.url
        return _("No Avatar")

    get_about_myself.short_description = _('About Myself')
    get_avatar.short_description = _('Avatar')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PlaylistItemInline(SummernoteInlineModelAdmin, admin.StackedInline):
    model = PlaylistItem
    extra = 1  # The number of extra forms in the inline formset.
    summernote_fields = ('description',)


class PlaylistItemAdmin(SummernoteModelAdmin):
    list_display = (
        'song_title', 'artist', 'album', 'playlist', 'performance_year')
    list_filter = ('artist', 'album', 'playlist')
    search_fields = ('song_title', 'artist')
    raw_id_fields = ('playlist',)
    summernote_fields = ('description',)


admin.site.register(PlaylistItem, PlaylistItemAdmin)


class PlaylistAdmin(SummernoteModelAdmin):
    list_display = (
        'id',
        'slug',
        'author',
        'created_on',
        'status',
        'display_featured_image'
    )
    list_filter = ('status', 'created_on')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    summernote_fields = ('description',)
    date_hierarchy = 'created_on'
    ordering = ('status', 'created_on')
    inlines = [PlaylistItemInline]

    # Custom method to display the clickable link in the admin
    def display_featured_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<a href="{0}">View Image</a>',
                obj.featured_image.url
            )
        return "No image"
    display_featured_image.short_description = 'Featured Image'


admin.site.register(Playlist, PlaylistAdmin)
