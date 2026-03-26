from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Match
from accounts.models import UserProfile
from spotify.models import SpotifyData
from django.contrib.auth.decorators import login_required

@login_required
def find_match(request):
    # Get profiles the current user has already swiped on
    already_swiped = Match.objects.filter(
        from_user=request.user
    ).values_list('to_user', flat=True)

    # Get current user's Spotify data
    my_spotify = SpotifyData.objects.filter(user=request.user).first()
    my_genres = set(my_spotify.top_genres) if my_spotify else set()
    my_artists = set(my_spotify.top_artists) if my_spotify else set()

    # Get candidate profiles (excluding self and already swiped)
    candidates = UserProfile.objects.exclude(
        user=request.user
    ).exclude(
        user__in=already_swiped
    ).select_related('user')

    # Score each candidate by shared genres + artists
    profile = None
    if candidates.exists():
        best_score = -1

        for candidate in candidates:
            candidate_spotify = SpotifyData.objects.filter(user=candidate.user).first()

            if candidate_spotify:
                shared_genres = len(my_genres & set(candidate_spotify.top_genres))
                shared_artists = len(my_artists & set(candidate_spotify.top_artists))
                score = (shared_genres * 2) + shared_artists  # genres weighted higher
            else:
                score = 0

            if score > best_score:
                best_score = score
                profile = candidate

    # Fetch Spotify data for the profile being shown
    spotify_data = None
    if profile:
        spotify_data = SpotifyData.objects.filter(user=profile.user).first()

        # Calculate compatibility stats to show in template
        shared_genres = sorted(my_genres & set(spotify_data.top_genres)) if spotify_data else []
        shared_artists = sorted(my_artists & set(spotify_data.top_artists)) if spotify_data else []
    else:
        shared_genres = []
        shared_artists = []

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')

        Match.objects.create(
            from_user=request.user,
            to_user_id=profile_id,
            action=action
        )

        if action == 'like':
            mutual = Match.objects.filter(
                from_user_id=profile_id,
                to_user=request.user,
                action='like'
            ).exists()

            if mutual:
                messages.success(request, "🎵 It's a Match! You're in tune!")

        return redirect('find_match')

    return render(request, 'find_match.html', {
        'profile': profile,
        'spotify_data': spotify_data,
        'shared_genres': shared_genres,
        'shared_artists': shared_artists,
    })