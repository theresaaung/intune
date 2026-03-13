from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .utils import get_spotify_oauth, fetch_and_save_spotify_data
from .models import SpotifyToken, SpotifyData

@login_required
def spotify_connect(request):
    """Redirects user to Spotify login page"""
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@login_required
def spotify_callback(request):
    """Spotify redirects back here after user logs in"""
    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')   # Spotify sends a code in the URL
    
    if not code:
        messages.error(request, 'Spotify connection failed.')
        return redirect('accounts:profile')

    # exchange the code for tokens
    token_info = sp_oauth.get_access_token(code)

    # save tokens to database
    SpotifyToken.objects.update_or_create(
        user=request.user,
        defaults={
            'access_token': token_info['access_token'],
            'refresh_token': token_info['refresh_token'],
            'token_expiry': timezone.now() + timedelta(seconds=token_info['expires_in']),
        }
    )

    # immediately fetch their spotify data
    fetch_and_save_spotify_data(request.user)
    messages.success(request, 'Spotify connected successfully!')
    return redirect('accounts:profile')

@login_required
def spotify_disconnect(request):
    """Removes stored tokens and data"""
    SpotifyToken.objects.filter(user=request.user).delete()
    SpotifyData.objects.filter(user=request.user).delete()
    messages.success(request, 'Spotify disconnected.')
    return redirect('accounts:profile')

@login_required
def spotify_refresh(request):
    """Manual refresh button — re-fetches Spotify data"""
    success = fetch_and_save_spotify_data(request.user)
    if success:
        messages.success(request, 'Spotify data refreshed!')
    else:
        messages.error(request, 'Could not refresh — is your Spotify connected?')
    return redirect('accounts:profile')