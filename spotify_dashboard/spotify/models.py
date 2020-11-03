import time

from django.db import models
from django.utils.timesince import timesince


class Track(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=500)
    last_played_at = models.DateTimeField()
    image = models.URLField()
    href = models.URLField()
    data = models.JSONField()

    class Meta:
        ordering = ('-last_played_at',)
        get_latest_by = "last_played_at"

    def __str__(self):
        return self.name


class Update(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = "created_at"

    def __str__(self):
        return "{0} ago".format(
            timesince(self.created_at))

    @property
    def unix_timestamp(self):
        return int(time.mktime(self.created_at.timetuple()))
