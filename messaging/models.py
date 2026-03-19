from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    """A single message sent between two matched users."""
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    match = models.ForeignKey(
        'matching.Match',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.body[:40]}"


class Notification(models.Model):
    """In-app notifications for new matches and new messages."""
    NOTIFICATION_TYPES = [
        ('new_match', 'New Match'),
        ('new_message', 'New Message'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.notification_type}] → {self.user.username}"