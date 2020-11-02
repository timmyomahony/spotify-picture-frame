import requests
import urllib
import logging

from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.conf import settings

from spotify.models import Code, AccessToken, Track

logger = logging.getLogger(__name__)


class SpotifyDashboard(TemplateView):
    template_name = "spotify/dashboard.html"


class SpotifyLatestAlbumArt(DetailView):
    """
    TODO: add JSON handling so we can refresh every X seconds
    """
    template_name = "spotify/latest_album_art.html"
    model = Track

    def get_object(queryset=None):
        return Track.objects.all().latest()


class SpotifyError(TemplateView):
    template_name = "spotify/error.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["error"] = self.request.GET.get('error', 'Unknown error')
        return context


class SpotifyAuth(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        params = urllib.parse.urlencode({
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'scope': settings.SPOTIFY_SCOPES,
            'redirect_uri': settings.SPOTIFY_REDIRECT
        })
        return "https://accounts.spotify.com/authorize?{0}".format(params)


class SpotifyAuthComplete(RedirectView):
    """
    Redirect end-point after authing with spotify. This view will receive the
    "code" query parameter, save it to the DB and redirect to the next step,
    creating a new access token
    """
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        value = self.request.GET.get('code')
        if not value:
            return "{0}?{1}".format(
                reverse('spotify:error'),
                urllib.parse.urlencode({
                    "error": "No 'code' query parameter present"
                }))
        code, created = Code.objects.get_or_create(value=value)
        logger.info('Code returned from Spotify: {0}'.format(value))
        logger.info('New code instance created: {0}'.format(created))
        return reverse('spotify:access-token')


class SpotifyAccessToken(RedirectView):
    """POST to the API with out latest "code" from the DB to return and save
    an access token"""
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        code = Code.objects.all().latest()
        logger.info('Code for access token: {0}'.format(code.value))
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code.value,
                "redirect_uri": settings.SPOTIFY_REDIRECT,
                "client_id": settings.SPOTIFY_CLIENT_ID,
                "client_secret": settings.SPOTIFY_SECRET_ID
            })
        content = response.json()
        logger.info('Spotify access token response: {0}'.format(content))
        if response.status_code == 200:
            access_token, created = AccessToken.objects.get_or_create(
                access_token=content['access_token'],
                scope=content['scope'],
                expires_in=content['expires_in'],
                refresh_token=content['refresh_token']
            )
            logger.info("Created new access token object: {0}".format(
                access_token.access_token))
        else:
            return "{0}?{1}".format(
                reverse('spotify:error'),
                urllib.parse.urlencode({
                    "error": content['error_description']
                }))
        return reverse('spotify:dashboard')
