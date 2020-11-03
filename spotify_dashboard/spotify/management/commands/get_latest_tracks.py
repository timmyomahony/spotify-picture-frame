import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from spotify.models import Update,Track


class Command(BaseCommand):
    help = 'Get latest 50 played spotify tracks'

    def handle(self, *args, **options):
        client = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=settings.SPOTIFY_SCOPES,
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_SECRET_ID,
            redirect_uri=settings.SPOTIFY_REDIRECT,
            open_browser=False))

        try:
            last_update = Update.objects.all().latest()
        except:
            last_update = None

        kwargs = {
            "limit": 50
        }
        if last_update:
            kwargs['after'] = last_update.unix_timestamp

        response = client._get('me/player/recently-played', **kwargs)

        for result in response['items']:
            played_at = datetime.datetime.strptime(result["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ") # 2016-12-13T20:42:17.016Z
            try:
                track = Track.objects.get(id=result["track"]["id"])
                track.last_played_at = played_at
                track.save()
            except Track.DoesNotExist:
                track = Track.objects.create(
                    id=result["track"]["id"],
                    name=result["track"]["name"],
                    href=result["track"]["href"],
                    last_played_at=played_at,
                    image=[img["url"] for img in result["track"]["album"]["images"]][0],
                    data=result)

        Update.objects.create()
