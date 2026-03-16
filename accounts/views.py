from django.shortcuts import render, redirect
from accounts.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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
     
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })   

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
            return render(request, 'accounts/login.html', {
                'error': "Invalid login details supplied."
            })
    
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'profile': profile
    })