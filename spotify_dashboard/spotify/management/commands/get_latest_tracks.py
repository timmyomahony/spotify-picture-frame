import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from spotify.models import Track


class Command(BaseCommand):
    help = 'Get latest 50 played spotify tracks'

    def handle(self, *args, **options):
        client = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=settings.SPOTIFY_SCOPES,
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_SECRET_ID,
            redirect_uri=settings.SPOTIFY_REDIRECT,
            open_browser=False))

        response = client._get('me/top/tracks', **{
            "limit": 50,
            "time_range": "short_term"
        })

        Track.objects.all().delete()

        for result in response['items']:
            try:
                Track.objects.get(id=result["id"])
            except Track.DoesNotExist:
                Track.objects.create(
                    id=result["id"],
                    title=result["name"],
                    album=result["album"]["name"],
                    artist=result["artists"][0]["name"],
                    href=result["href"],
                    image=[img["url"] for img in result["album"]["images"]][0],
                    data=result)