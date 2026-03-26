from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse

from matching.models import Match
from .models import Message, Notification
from .forms import MessageForm


def get_mutual_match(user1, user2):
    """Returns a Match object only if both users liked each other."""
    user1_liked = Match.objects.filter(from_user=user1, to_user=user2, action='like').exists()
    user2_liked = Match.objects.filter(from_user=user2, to_user=user1, action='like').exists()
    if user1_liked and user2_liked:
        return Match.objects.filter(from_user=user1, to_user=user2, action='like').first()
    return None


def create_notification(user, notification_type, text, link=''):
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        text=text,
        link=link,
    )


@login_required
def inbox(request):
    liked_you_ids = Match.objects.filter(
        to_user=request.user, action='like'
    ).values_list('from_user', flat=True)

    mutual_ids = Match.objects.filter(
        from_user=request.user,
        to_user__in=liked_you_ids,
        action='like'
    ).values_list('to_user', flat=True)

    mutual_users = User.objects.filter(id__in=mutual_ids)

    conversations = []
    for other_user in mutual_users:
        match = Match.objects.filter(
            from_user=request.user, to_user=other_user, action='like'
        ).first()

        last_message = Message.objects.filter(
            Q(sender=request.user, recipient=other_user) |
            Q(sender=other_user, recipient=request.user)
        ).order_by('-timestamp').first()

        unread_count = Message.objects.filter(
            sender=other_user,
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

    total_unread = sum(c['unread_count'] for c in conversations)

    return render(request, 'inbox.html', {
        'conversations': conversations,
        'unread_count': total_unread,
    })


@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    match = get_mutual_match(request.user, other_user)
    if not match:
        return render(request, 'not_matched.html', {'other_user': other_user})

    Message.objects.filter(
        sender=other_user,
        recipient=request.user,
        is_read=False,
    ).update(is_read=True)

    messages_qs = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')

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
    return render(request, 'conversation.html', context)


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-timestamp')
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifs})


@login_required
def unread_notification_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})