from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from datetime import datetime
from .models import YapsterUser, User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.core.files.base import File

"""
@login_required
def update_profile(request):
    user = request.user
    yapster_user = user.yapsteruser

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=yapster_user)
        if form.is_valid():
            form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('profile_page')
    else:
        form = ProfileUpdateForm(instance=yapster_user)
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['email'].initial = user.email

    return render(request, 'update_profile.html', {'form': form, 'user': user})
"""
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.yapsteruser)
        if form.is_valid():
            yapster_user = form.save(commit=False)
            user = yapster_user.user
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if 'profile_image' in request.FILES:
                yapster_user.profile_image = request.FILES['profile_image']
            user.save()
            yapster_user.save()
            return redirect('profile_page')
    else:
        form = ProfileForm(instance=request.user.yapsteruser)
    return render(request, 'profile_settings.html', {'form': form})

def landing_page_view(request):
    return render(request, 'landing_page.html')

def index_view(request):
    if request.user.is_authenticated:
        return redirect('chat')
    return redirect('landing_page')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username exists')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        user_login = auth.authenticate(username=username, password=password)

        if user_login is not None:
            auth.login(request, user_login)
            user = YapsterUser.objects.create(user=user)
            user.save()
            request.session['logged_user'] = user.id
            print(user.id)
            return redirect('chat')
        else:
            messages.info(request, 'Error after registration.')
            return redirect('login')
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if ("@" and ".com") in username:
            user_obj = User.objects.filter(email=username).first()
            user_login = auth.authenticate(username=user_obj, password=password)
        else:
            user_obj = User.objects.filter(username=username).first()
            user_login = auth.authenticate(username=username, password=password)

        # TO ADD: Notif for incorrect password

        if user_login is not None:
            auth.login(request, user_login)
            request.session['logged_user'] = user_obj.id
            print(user_obj.id)
            return redirect('chat')
        else:
            messages.info(request, 'Incorrect username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def chat_view(request):
    return render(request, 'chat_view.html')

@login_required
def update_user(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.yapsteruser)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    else:
        form = ProfileForm(instance=request.user.yapsteruser)
        #form.fields['email'].initial = request.user.email
        # form.fields['birthdate'].initial = request.user.yapsteruser.birthdate
        #form.fields['gender'].initial = request.user.yapsteruser.gender
    return render(request, 'profile_settings.html', {'user': request.user, 'form': form})

@login_required
def delete_user(request):
    user = request.user
    user.is_deleted = True
    user.save()
    return redirect('logout')


def profile_page(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.yapsteruser)
        if form.is_valid():
            form.save()
            return redirect('profile_settings')
    else:
        form = ProfileForm(instance=request.user.yapsteruser)

    return render(request, 'profile_settings.html', {'form': form})

@login_required
def view_public_profile(request):
    user = get_object_or_404(YapsterUser, user=request.user)
    return render(request, 'public_profile.html', {'yapster_user': user})

@login_required
def public_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    yapster_user = user.yapsteruser
    return render(request, 'public_profile.html', {'user': user, 'yapster_user': yapster_user})

