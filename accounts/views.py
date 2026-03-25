from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserForm, UserProfileForm, PhotoUploadForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile, Photo
from spotify.models import SpotifyToken
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
     
    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    }
    return render(request, 'accounts/register.html', context_dict)   

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('profile')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            context_dict = {'error': "Invalid login details supplied."}
            return render(request, 'accounts/login.html', context_dict)
    
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user) 
    spotify_connected = SpotifyToken.objects.filter(user=request.user).exists()
    photos = request.user.photos.all()
    context_dict = {
        'profile': profile,
        'spotify_connected': spotify_connected,
        'photos': photos,
        }
    return render(request, 'accounts/profile.html', context_dict)

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        if "save_profile" in request.POST:
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            photo_form = PhotoUploadForm()
            if form.is_valid():
                form.save()
                return redirect('profile')
        if "upload_photo" in request.POST:
            form = UserProfileForm(instance=profile)
            photo_form = PhotoUploadForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.user = request.user
                photo.save()
                return redirect('edit_profile')           
    else:
        form = UserProfileForm(instance=profile)
        photo_form = PhotoUploadForm()
    photos = request.user.photos.all()
    context_dict = {
        'form': form,
        'photo_form': photo_form,
        'photos': photos,
        }
    return render(request, 'accounts/edit_profile.html', context_dict)

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photo.delete()
    return redirect("edit_profile")

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'accounts/delete_account.html')

@login_required
def view_user(request, username):
    user = User.objects.get(username=username)
    profile = user.userprofile  
    photos = request.user.photos.all() 
    context_dict = {
        'profile': profile,
        'photos': photos,
                    }
    return render(request, 'accounts/view_user.html', context_dict)