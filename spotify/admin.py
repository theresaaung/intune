from django.contrib import admin
from .models import SpotifyToken, SpotifyData

admin.site.register(SpotifyToken)
admin.site.register(SpotifyData)
