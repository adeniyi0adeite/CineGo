# videos/models


from django.db import models
from django.conf import settings
from hashids import Hashids
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Video(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('drama', 'Drama'),
        ('comedy', 'Comedy'),
        ('horror', 'Horror'),
        ('thriller', 'Thriller'),
        # Add more genres as needed
    ]
    
    PARENTAL_GUIDANCE_CHOICES = [
        ('G', 'General Audience'),
        ('PG', 'Parental Guidance'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
    ]

    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos_uploads/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    parental_guidance = models.CharField(max_length=10, choices=PARENTAL_GUIDANCE_CHOICES)
    running_time = models.DurationField(default=timedelta(minutes=0))
    premiere_date = models.DateField(null=True, blank=True)
    director = models.ForeignKey('users.Director', on_delete=models.SET_NULL, null=True, related_name='directed_videos')
    actors = models.ManyToManyField('users.Actor', related_name='movies_set')
    description = models.TextField(blank=True, null=True)
    artwork = models.ImageField(upload_to='artworks/', blank=True, null=True)
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    release_date = models.DateField(default=timezone.now)
    upload_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', related_name="videos", blank=True)
    movie_type = models.CharField(max_length=50, choices=[('Movie', 'Movie'), ('TV Series', 'TV Series')], blank=True, null=True)


    def generate_link(self):
        """Generate a unique, time-sensitive link for the video."""
        hashids = Hashids(salt=settings.HASHIDS_SALT, min_length=8)
        return hashids.encode(self.id)

    def is_link_valid(self):
        """Check if the video link is still valid (24 hours after upload)."""
        expiry_time = self.upload_time + timedelta(hours=24)
        return timezone.now() < expiry_time

    def __str__(self):
        return self.title



@receiver(post_save, sender=Video)
def update_actor_and_director_videos(sender, instance, created, **kwargs):
    """Signal to update the actors' and directors' video lists whenever a Video is created or updated."""
    # Update director relationship
    if instance.director:
        instance.director.videos.add(instance)
    
    # Update actors relationship
    for actor in instance.actors.all():
        actor.videos.add(instance)




class VideoAccess(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    access_granted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} has access to {self.video}"

