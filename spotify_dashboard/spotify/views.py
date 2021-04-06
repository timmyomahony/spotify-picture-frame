import logging

from django.views.generic.list import ListView
from spotify.models import Track

logger = logging.getLogger(__name__)


class SpotifyLatestAlbumArt(ListView):
    template_name = "spotify/latest_album_art.html"
    model = Track

    def get_queryset(self, **kwargs):
        return Track.objects.filter(published=True).order_by("?")
