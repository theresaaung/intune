from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from matching.models import Match
from .models import Message, Notification
from .forms import MessageForm


def get_match_for_users(user1, user2):
    return Match.objects.filter(
        Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
    ).first()


def create_notification(user, notification_type, text, link=''):
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        text=text,
        link=link,
    )


@login_required
def inbox(request):
    matches = Match.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).order_by('-created_at')

    conversations = []
    for match in matches:
        other_user = match.user2 if match.user1 == request.user else match.user1

        last_message = (
            Message.objects.filter(match=match)
            .order_by('-timestamp')
            .first()
        )

        unread_count = Message.objects.filter(
            match=match,
            recipient=request.user,
            is_read=False,
        ).count()

        conversations.append({
            'match': match,
            'other_user': other_user,
            'last_message': last_message,
            'unread_count': unread_count,
        })

    conversations.sort(
        key=lambda c: c['last_message'].timestamp if c['last_message'] else c['match'].created_at,
        reverse=True,
    )

    Notification.objects.filter(
        user=request.user,
        notification_type='new_message',
        is_read=False,
    ).update(is_read=True)

    return render(request, 'messaging/inbox.html', {'conversations': conversations})


@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    match = get_match_for_users(request.user, other_user)
    if not match:
        return render(request, 'messaging/not_matched.html', {'other_user': other_user})

    Message.objects.filter(
        match=match,
        recipient=request.user,
        is_read=False,
    ).update(is_read=True)

    messages_qs = Message.objects.filter(match=match).order_by('timestamp')

    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = other_user
            msg.match = match
            msg.save()

            create_notification(
                user=other_user,
                notification_type='new_message',
                text=f"New message from {request.user.username}",
                link=f"/messaging/conversation/{request.user.username}/",
            )

            return redirect('messaging:conversation', username=username)

    context = {
        'other_user': other_user,
        'messages': messages_qs,
        'form': form,
        'match': match,
    }
    return render(request, 'messaging/conversation.html', context)


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-timestamp')
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'messaging/notifications.html', {'notifications': notifs})


@login_required
def unread_notification_count(request):
    from django.http import JsonResponse
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})