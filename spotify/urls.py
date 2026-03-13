from django.urls import path
from . import views

app_name = 'spotify'

urlpatterns = [
    path('connect/', views.spotify_connect, name='connect'),
    path('callback/', views.spotify_callback, name='callback'),
    path('disconnect/', views.spotify_disconnect, name='disconnect'),
    path('refresh/', views.spotify_refresh, name='refresh'),
]