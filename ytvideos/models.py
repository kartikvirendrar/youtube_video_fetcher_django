from django.db import models

class Video(models.Model):
    title = models.TextField(blank=False)
    description = models.TextField()
    publishing_datetime = models.DateTimeField()
    thumbnail_url = models.URLField()
    video_id = models.CharField(unique=True, blank=False)