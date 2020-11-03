from django.urls import path

from spotify_dashboard.spotify.views import SpotifyLatestAlbumArt

app_name = "spotify"
urlpatterns = [
    path("", view=SpotifyLatestAlbumArt.as_view(), name="latest-album-art"),
]
