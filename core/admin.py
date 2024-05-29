from django.contrib import admin
from .models import PlaylistPost, Comment


class PlaylistPostAdmin(admin.ModelAdmin):
    list_display = (
        'playlist',
        'author_username',
        'created_on',
        'updated_on',
        'total_likes'
    )
    search_fields = ('playlist', 'created_on')
    list_filter = ('created_on', 'updated_on')

    def author_username(self, obj):
        return obj.playlist.author.username
    author_username.short_description = 'Author'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'playlist_post', 'author', 'created_on', 'total_likes_comment')
    list_filter = ('created_on', 'author')
    search_fields = ('playlist_post', 'author')


admin.site.register(PlaylistPost, PlaylistPostAdmin)
admin.site.register(Comment, CommentAdmin)
