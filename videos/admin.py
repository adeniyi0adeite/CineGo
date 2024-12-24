from django.contrib import admin
from .models import Video, VideoAccess
from django.utils.html import format_html

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'upload_time', 'generate_link', 'is_link_valid', 'video_file_preview', 'duration', 'release_date')
    search_fields = ('title', 'user__username')
    list_filter = ('user', 'upload_time', 'release_date')
    ordering = ('-upload_time',)

    def video_file_preview(self, obj):
        """Generate a preview for the uploaded video file."""
        return format_html('<a href="{}" target="_blank">Preview</a>', obj.video_file.url)
    video_file_preview.short_description = 'Video File Preview'

    def generate_link(self, obj):
        """Display the generated link for the video."""
        return obj.generate_link()
    generate_link.short_description = 'Generated Link'

    def is_link_valid(self, obj):
        """Check if the link for the video is still valid."""
        return obj.is_link_valid()
    is_link_valid.boolean = True
    is_link_valid.short_description = 'Link Valid'

class VideoAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'access_granted_at')
    search_fields = ('user__username', 'video__title')
    list_filter = ('user', 'video')
    ordering = ('-access_granted_at',)

    def user_link(self, obj):
        """Display a clickable link to the user's profile."""
        return format_html('<a href="{}">{}</a>', f"/admin/users/userprofile/{obj.user.id}/change/", obj.user.username)
    user_link.short_description = 'User Profile'


# Register the models with the custom admin
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoAccess, VideoAccessAdmin)
