from django.contrib import admin
from .models import Video, VideoAccess, Category
from django.utils.html import format_html

class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'release_date', 'upload_time', 'duration', 
        'category', 'video_file_preview', 'generate_link', 'is_link_valid'
    )
    search_fields = ('title', 'actors__full_name', 'director__full_name')
    list_filter = ('genre', 'release_date', 'premiere_date', 'categories')  # Use premiere_date instead of premiere
    ordering = ('-upload_time',)

    def video_file_preview(self, obj):
        """Generate a preview link for the uploaded video file."""
        return format_html('<a href="{}" target="_blank">Preview</a>', obj.video_file.url)
    video_file_preview.short_description = 'Video File Preview'

    def generate_link(self, obj):
        """Display the generated unique link for the video."""
        return obj.generate_link()
    generate_link.short_description = 'Generated Link'

    def is_link_valid(self, obj):
        """Check if the link for the video is still valid."""
        return obj.is_link_valid()
    is_link_valid.boolean = True
    is_link_valid.short_description = 'Link Valid'

    def category(self, obj):
        """Display the categories associated with the video."""
        return ", ".join([category.name for category in obj.categories.all()])
    category.short_description = 'Categories'

    def duration(self, obj):
        """Display the duration of the video."""
        return str(obj.running_time)
    duration.short_description = 'Duration'


class VideoAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'access_granted_at')
    search_fields = ('user__username', 'video__title')
    list_filter = ('user', 'video', 'access_granted_at')
    ordering = ('-access_granted_at',)

    def user_link(self, obj):
        """Display a clickable link to the user's profile."""
        return format_html('<a href="{}">{}</a>', f"/admin/users/userprofile/{obj.user.id}/change/", obj.user.username)
    user_link.short_description = 'User Profile'

# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)

# Register the models with the custom admin
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoAccess, VideoAccessAdmin)
admin.site.register(Category, CategoryAdmin)
