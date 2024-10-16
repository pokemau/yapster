from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from datetime import datetime
from .models import YapsterUser, User
from .forms import UpdateUserForm
from django.contrib.auth.decorators import login_required


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

        user = User.objects.create_user(username=username,
                                        password=password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        user_login = auth.authenticate(username=username, password=password)

        if user_login is not None:
            auth.login(request, user_login)
            yapster_user = YapsterUser.objects.create(user=user)
            yapster_user.save()
            request.session['logged_user'] = yapster_user.id
            print(yapster_user.id)
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
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    else:
        form = UpdateUserForm(instance=request.user)
        form.fields['birthdate'].initial = request.user.yapsteruser.birthdate
        form.fields['gender'].initial = request.user.yapsteruser.gender
    return render(request, 'profile_page.html', {'user': request.user, 'form': form})


@login_required
def delete_user(request):
    user = request.user
    user.is_deleted = True
    user.save()
    return redirect('logout')


@login_required
def profile_page(request):
    form = UpdateUserForm(instance=request.user)
    return render(request, 'profile_page.html', {'user': request.user, 'form': form})