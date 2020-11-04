import time

from django.db import models
from django.utils.timesince import timesince


class Track(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    artist = models.CharField(max_length=500)
    album = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    image = models.URLField()
    href = models.URLField()
    data = models.JSONField()
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
