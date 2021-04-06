import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from spotify.models import Track


class Command(BaseCommand):
    help = 'Print devices'

    def handle(self, *args, **options):
        client = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=settings.SPOTIFY_SCOPES,
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_SECRET_ID,
            redirect_uri=settings.SPOTIFY_REDIRECT,
            open_browser=False))

        response = client._get('me/player/devices', **{})

        print(response)