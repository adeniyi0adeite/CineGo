from django.db import models
from django.conf import settings
from hashids import Hashids
from django.utils import timezone
from datetime import timedelta

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos_uploads/')
    upload_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)

    def generate_link(self):
        hashids = Hashids(salt=settings.HASHIDS_SALT, min_length=8)
        return hashids.encode(self.id)

    def is_link_valid(self):
        # Example: Link expires after 24 hours
        expiry_time = self.upload_time + timedelta(hours=24)
        return timezone.now() < expiry_time
