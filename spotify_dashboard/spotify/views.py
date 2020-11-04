import requests
import urllib
import logging

from django.views.generic.list import ListView
from django.urls import reverse
from django.conf import settings

from spotify.models import Track

logger = logging.getLogger(__name__)


class SpotifyLatestAlbumArt(ListView):
    template_name = "spotify/latest_album_art.html"
    model = Track

    def get_queryset(queryset=None):
        return Track.objects.filter(published=True).order_by("?")