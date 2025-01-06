# users/models


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_fullname(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

    def get_active_subscription(self):
        """Returns the active subscription plan for the user if it exists."""
        active_subscription = self.subscriptions.filter(end_date__gte=timezone.now()).first()
        return active_subscription if active_subscription else None

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()






class Actor(models.Model):
    full_name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='actor_photos/profile', blank=True, null=True)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    about = models.TextField(blank=True, null=True)

    # New photo album field with modified related_name to avoid conflicts
    photos_album = models.ManyToManyField('ActorPhoto', related_name='albums', blank=True)  # Changed related_name



    videos = models.ManyToManyField('videos.Video', related_name='actors_set', blank=True)  # Changed related_name

    def age(self):
        """Autogenerate actor's age based on their date of birth."""
        return relativedelta(timezone.now().date(), self.date_of_birth).years

    def total_movies(self):
        """Return the total number of movies the actor has appeared in."""
        return self.videos.count()

    def first_movie(self):
        """Return the first movie the actor appeared in.""" 
        return self.videos.order_by('release_date').first()

    def last_movie(self):
        """Return the last movie the actor appeared in."""
        return self.videos.order_by('-release_date').first()

    def __str__(self):
        return self.full_name


class ActorPhoto(models.Model):
    actor = models.ForeignKey(Actor, related_name='actor_photos', on_delete=models.CASCADE)  # Changed related_name
    photo = models.ImageField(upload_to='actor_photos/album')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Photo for {self.actor.full_name} - {self.caption or 'No caption'}"
    


@receiver(post_save, sender=ActorPhoto)
def add_photo_to_actor_album(sender, instance, created, **kwargs):
    """Automatically add the photo to the actor's album after the photo is saved."""
    # Add the photo to the actor's photos_album
    if instance.actor and instance not in instance.actor.photos_album.all():
        instance.actor.photos_album.add(instance)


class Director(models.Model):
    full_name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='director_photos/profile', blank=True, null=True)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    about = models.TextField(blank=True, null=True)

    photos_album = models.ManyToManyField('DirectorPhoto', related_name='albums', blank=True)  # Changed related_name



    videos = models.ManyToManyField('videos.Video', related_name='directors', blank=True)  # Many-to-many relationship with Video

    def age(self):
        """Autogenerate director's age based on their date of birth."""
        return relativedelta(timezone.now().date(), self.date_of_birth).years

    def total_movies(self):
        """Return the total number of movies the director has directed."""
        return self.videos.count()

    def first_movie(self):
        """Return the first movie the director directed."""
        return self.videos.order_by('release_date').first()

    def last_movie(self):
        """Return the last movie the director directed."""
        return self.videos.order_by('-release_date').first()

    def __str__(self):
        return self.full_name
    

class DirectorPhoto(models.Model):
    director = models.ForeignKey(Director, related_name='director_photos', on_delete=models.CASCADE)  # Changed related_name
    photo = models.ImageField(upload_to='director_photos/album')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Photo for {self.director.full_name} - {self.caption or 'No caption'}"
    

@receiver(post_save, sender=DirectorPhoto)
def add_photo_to_director_album(sender, instance, created, **kwargs):
    """Automatically add the photo to the actor's album after the photo is saved."""
    # Add the photo to the actor's photos_album
    if instance.director and instance not in instance.director.photos_album.all():
        instance.director.photos_album.add(instance)


