import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from spotify.models import AccessToken, Update, Album, Track, Artist


class Command(BaseCommand):
    help = 'Get latest 50 played spotify tracks'

    def handle(self, *args, **options):
        """
        TODO: handle refresh tokens
        """
        # try:
        #     access_token = AccessToken.objects.latest()
        # except AccessToken.DoesNotExist:
        #     self.stdout.write(
        #         self.style.ERROR('No access token saved, please auth with Spotify first'))

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

        # client = spotipy.Spotify(auth=access_token.access_token)
        kwargs = {
            "limit": 50
        }
        if last_update:
            kwargs['after'] = last_update.unix_timestamp
        response = client._get('me/player/recently-played', **kwargs)

        for result in response['items']:
            artist_name = [artist["name"] for artist in result["track"]["artists"]][0]
            album_name = result["track"]["album"]["name"]

            artist, created = Artist.objects.get_or_create(
                name=artist_name)
            album, created = Album.objects.get_or_create(
                name=album_name,
                artist=artist
            )

            track_name = result["track"]["name"]
            duration_ms = int(result["track"]["duration_ms"])
            track_number = int(result["track"]["track_number"])
            played_at = datetime.datetime.strptime(result["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")  # 2016-12-13T20:42:17.016Z
            href = result["track"]["href"]
            image = [img["url"] for img in result["track"]["album"]["images"]][0]

            track, created = Track.objects.get_or_create(
                name=track_name,
                album=album,
                duration_ms=duration_ms,
                track_number=track_number,
                href=href,
                played_at=played_at,
                image=image,
                data=result)

        Update.objects.create()
