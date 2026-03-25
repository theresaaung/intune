from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    LOOKING_FOR_CHOICES = [
        ('romantic','Romantic'),
        ('platonic','Platonic'),
        ('both','Both'),
    ]
    MATCHING_PREFERENCE_CHOICES = [
        ('top_artists','Top Artists'),
        ('genre','Genre'),
        ('era','Era'),
        ('opposite_genre','Opposite Genre'),
    ]
    GENDER_CHOICES = [
        ('male','Male'),
        ('female','Female'),
        ('non_binary','Non-Binary'),
        ('prefer_not_to_say','Prefer Not to Say'),
    ]
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=False, blank=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    looking_for = models.CharField(max_length=20, choices=LOOKING_FOR_CHOICES, blank=True)
    matching_preference = models.CharField(max_length=20, choices=MATCHING_PREFERENCE_CHOICES, blank=True)


    preferred_min_age = models.IntegerField(null=True, blank=True)
    preferred_max_age = models.IntegerField(null=True, blank=True)
    preferred_gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    preferred_location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="profile_photos/")
    
    def __str__(self):
        return f"{self.user.username} Photo"