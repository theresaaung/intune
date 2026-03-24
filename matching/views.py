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

    # Get the next profile to show (excluding themselves and already swiped)
    profile = UserProfile.objects.exclude(
        user=request.user
    ).exclude(
        user__in=already_swiped
    ).first()

    # Fetch Spotify data for the profile being shown
    spotify_data = None
    if profile:
        spotify_data = SpotifyData.objects.filter(user=profile.user).first()

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')

        # Save the swipe
        Match.objects.create(
            from_user=request.user,
            to_user_id=profile_id,
            action=action
        )

        # Check if it's a mutual match
        if action == 'like':
            mutual = Match.objects.filter(
                from_user_id=profile_id,
                to_user=request.user,
                action='like'
            ).exists()

            if mutual:
                messages.success(request, "🎵 It's a Match! You're in tune!")
                return redirect('find_match')

        return redirect('find_match')

    return render(request, 'find_match.html', {
        'profile': profile,
        'spotify_data': spotify_data,
    })
