from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'display_name',
            'bio',
            'age',
            'gender',
            'location',
            'profile_picture',
            'looking_for',
            'matching_preference',
            'preferred_min_age',
            'preferred_max_age',
            'preferred_gender',
            'preferred_location',
        )