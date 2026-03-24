from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Match(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    action = models.CharField(max_length=10)  # 'like' or 'pass'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # prevents duplicate swipes