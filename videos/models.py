from django.db import models
from django.conf import settings
from hashids import Hashids
from django.utils import timezone
from datetime import timedelta

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos_uploads/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upload_time = models.DateTimeField(auto_now_add=True)
    release_date = models.DateField(default=timezone.now)  # Field for release date
    duration = models.DurationField(default=timedelta(minutes=0))  # Field for video duration
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    free_watch_time = models.DurationField(default=timedelta(seconds=4))  # New field for free watch time

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

class VideoAccess(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    access_granted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} has access to {self.video}"

