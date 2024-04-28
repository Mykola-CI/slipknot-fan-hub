from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.translation import gettext_lazy as _


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


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
