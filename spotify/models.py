from django.db import models
from django.contrib.auth.models import User

class SpotifyToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    token_expiry = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username}'s Spotify Token"

class SpotifyData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    top_artists = models.JSONField(default=list)   # stores list of artist names
    top_genres = models.JSONField(default=list)    # stores list of genre names
    top_tracks = models.JSONField(default=list)    # stores list of track info
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Spotify Data"