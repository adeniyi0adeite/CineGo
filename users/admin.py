from django.contrib import admin
from .models import UserProfile, Actor, Director, ActorPhoto, DirectorPhoto
from videos.models import Video

# Inline Model for ActorPhoto
class ActorPhotoInline(admin.TabularInline):
    model = Actor.photos_album.through  # This is the join model for Many-to-Many relationship
    extra = 1  # Add an extra empty form for adding new ActorPhoto

# Inline Model for DirectorPhoto
class DirectorPhotoInline(admin.TabularInline):
    model = Director.photos_album.through  # This is the join model for Many-to-Many relationship
    extra = 1  # Add an extra empty form for adding new DirectorPhoto

# Admin for Actor
class ActorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'calculate_age', 'total_movies', 'first_movie', 'last_movie', 'get_videos')
    search_fields = ('full_name', 'genres', 'place_of_birth')
    list_filter = ('genres',)
    inlines = [ActorPhotoInline]  # Add inline to manage photos directly from the actor form

    def calculate_age(self, obj):
        """Get the calculated age of the actor."""
        return obj.age()
    calculate_age.short_description = 'Age'

    def total_movies(self, obj):
        """Get the total number of movies for the actor."""
        return obj.total_movies()
    total_movies.short_description = 'Total Movies'

    def get_videos(self, obj):
        """Display the list of videos associated with the actor."""
        return ", ".join([video.title for video in obj.videos.all()])
    get_videos.short_description = 'Videos'

# Admin for Director
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'calculate_age', 'total_movies', 'first_movie', 'last_movie', 'get_videos')
    search_fields = ('full_name', 'genres', 'place_of_birth')
    list_filter = ('genres',)
    inlines = [DirectorPhotoInline]  # Add inline to manage photos directly from the director form

    def calculate_age(self, obj):
        """Get the calculated age of the director."""
        return obj.age()
    calculate_age.short_description = 'Age'

    def total_movies(self, obj):
        """Get the total number of movies for the director."""
        return obj.total_movies()
    total_movies.short_description = 'Total Movies'

    def get_videos(self, obj):
        """Display the list of videos associated with the director."""
        return ", ".join([video.title for video in obj.videos.all()])
    get_videos.short_description = 'Videos'

# Admin for ActorPhoto
class ActorPhotoAdmin(admin.ModelAdmin):
    list_display = ('actor', 'photo', 'caption')
    search_fields = ('actor__full_name', 'caption')

# Admin for DirectorPhoto
class DirectorPhotoAdmin(admin.ModelAdmin):
    list_display = ('director', 'photo', 'caption')
    search_fields = ('director__full_name', 'caption')

# Register models with admin
admin.site.register(UserProfile)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(ActorPhoto, ActorPhotoAdmin)
admin.site.register(DirectorPhoto, DirectorPhotoAdmin)
