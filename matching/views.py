from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages #NEEDS LINKED TO MESSAGES
from .models import Match
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

#@login_required ADD BACK LATER
def find_match(request):
    test_user = User.objects.first() # REMOVE LATER
    # Get profiles the current user has already swiped on
    already_swiped = Match.objects.filter(
        #from_user=request.user CHANGE LATER
        from_user=test_user
    ).values_list('to_user', flat=True)

    # Get the next profile to show (excluding themselves and already swiped)
    profile = UserProfile.objects.exclude(
        #user=request.user CHANGE LATER
        user=test_user 
    ).exclude(
        user__in=already_swiped
    ).first()

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')

        # Save the swipe
        Match.objects.create(
            #from_user=request.user, CHANGE LATER
            from_user=test_user,
            to_user_id=profile_id,
            action=action
        )

        # Check if it's a mutual match
        if action == 'like':
            mutual = Match.objects.filter(
                from_user_id=profile_id,
                #to_user=request.user, CHANGE LATER
                to_user=test_user,
                action='like'
            ).exists()

            if mutual:
                messages.success(request, "🎵 It's a Match! You're in tune!")
                return redirect('messages')  # redirect to your messages NEEDS LINKED 

        return redirect('find_match')  # load the next profile 

    return render(request, 'find_match.html', {'profile': profile})