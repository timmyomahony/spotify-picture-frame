from django.urls import path

from spotify_dashboard.spotify.views import (
    SpotifyAuth, SpotifyDashboard, SpotifyAuthComplete, SpotifyAccessToken,
    SpotifyError, SpotifyLatestAlbumArt)

app_name = "spotify"
urlpatterns = [
    path("", view=SpotifyDashboard.as_view(), name="dashboard"),
    #path("error/", view=SpotifyError.as_view(), name="error"),
    #path("auth/", view=SpotifyAuth.as_view(), name="auth"),
    #path("auth-complete/", view=SpotifyAuthComplete.as_view(), name="auth-complete"),
    path("access-token/", view=SpotifyAccessToken.as_view(), name="access-token"),
    #path("latest-album-art/", view=SpotifyLatestAlbumArt.as_view(), name="latest-album-art"),
]
