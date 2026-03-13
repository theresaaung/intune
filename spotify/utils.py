import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import SpotifyToken, SpotifyData

def get_spotify_oauth():
    """Creates the OAuth object — used when logging in with Spotify"""
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope='user-top-read',   # only need read access to top tracks/artists
    )

def get_spotify_client(user):
    """Gets an authenticated Spotify client for a specific user"""
    try:
        token = SpotifyToken.objects.get(user=user)
        # check if token is expired and refresh if needed
        if token.token_expiry <= timezone.now():
            sp_oauth = get_spotify_oauth()
            new_token = sp_oauth.refresh_access_token(token.refresh_token)
            token.access_token = new_token['access_token']
            token.token_expiry = timezone.now() + timedelta(seconds=new_token['expires_in'])
            token.save()
        return spotipy.Spotify(auth=token.access_token)
    except SpotifyToken.DoesNotExist:
        return None

def fetch_and_save_spotify_data(user):
    """Fetches top artists, genres and tracks from Spotify and saves to DB"""
    sp = get_spotify_client(user)
    if not sp:
        return False

    # fetch top artists
    top_artists_data = sp.current_user_top_artists(limit=10, time_range='medium_term')
    top_artists = [artist['name'] for artist in top_artists_data['items']]

    # extract genres from artists
    top_genres = []
    for artist in top_artists_data['items']:
        top_genres.extend(artist['genres'])
    top_genres = list(set(top_genres))   # remove duplicates

    # fetch top tracks
    top_tracks_data = sp.current_user_top_tracks(limit=10, time_range='medium_term')
    top_tracks = [
        {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'year': track['album']['release_date'][:4]   # just the year
        }
        for track in top_tracks_data['items']
    ]

    # save to database
    SpotifyData.objects.update_or_create(
        user=user,
        defaults={
            'top_artists': top_artists,
            'top_genres': top_genres,
            'top_tracks': top_tracks,
        }
    )
    return True