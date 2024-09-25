from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from datetime import datetime
from .models import YapsterUser


def index_view(request):
    """ (mau)
    - diri nga view i check if logged in ang user or not
    - if logged in ay redirect to home
    - if not logged in kay redirect to login_view
    """
    return redirect('login')

def register_view(request):
    """
    TODO
        - check if valid ang birthdate
    """
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        gender = request.POST['gender']
        birthday = datetime.strptime(request.POST['birthday'], "%Y-%m-%d")

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
                user.first_name = fname
                user.last_name = lname
                user.save()

                # login user
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request, user_login)

                user_ref = User.objects.get(username=username)
                yapster_user = YapsterUser.objects.create(user=user_ref)
                yapster_user.birthdate = birthday
                yapster_user.gender = gender
                yapster_user.save()

                # TODO
                # redirect to home_view / chat_view
                return redirect('chat')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_login = auth.authenticate(username=username,password=password)

        if user_login is not None:
            auth.login(request, user_login)
            return redirect('chat')
        else:
            messages.info(request, 'Incorrect username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def chat_view(request):
    return render(request, 'chat_view.html')