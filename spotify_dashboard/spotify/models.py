import time

from django.db import models
from django.utils.timesince import timesince


class Code(models.Model):
    value = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = "created_at"

    def __str__(self):
        return "{0} ago".format(
            timesince(self.created_at))


class AccessToken(models.Model):
    access_token = models.CharField(max_length=1024)
    scope = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=1024)
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = "created_at"

    def __str__(self):
        return "{0} ago".format(
            timesince(self.created_at))


class Artist(models.Model):
    name = models.CharField(max_length=256)


class Album(models.Model):
    name = models.CharField(max_length=256)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)


class Track(models.Model):
    name = models.CharField(max_length=500)
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    duration_ms = models.IntegerField()
    track_number = models.IntegerField()
    played_at = models.DateTimeField()
    image = models.URLField()
    href = models.URLField()

    data = models.JSONField()

    class Meta:
        ordering = ('-played_at',)
        get_latest_by = "played_at"

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
