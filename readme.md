# Quickstart

Create/update the Spotify app on their dashboard

https://developer.spotify.com/dashboard/applications/

Create a `.env`:

```sh
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython

SPOTIFY_CLIENT_ID=
SPOTIFY_SECRET_ID=
SPOTIFY_REDIRECT=http://localhost:8000/auth-complete/
SPOTIFY_SCOPES=user-read-recently-played user-read-playback-state user-top-read
```

```sh
docker-compose up --build
```

And to update get the latest tracks:

```sh
sudo docker-compose run --rm django python manage.py get_latest_tracks
```
