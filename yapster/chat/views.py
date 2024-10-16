from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from chat.models import Message, YapsterUser
from user.models import User

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'chat.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def test_chat_view(request):
    # check if logged in need verify na login si user
    # need nay chat na na belong (pwede default chat)
    if request.method=="POST":
        content = request.POST["message_to_send"]
        if 'logged_user' in request.session:
            sender = User.objects.get(id=request.session['logged_user'])
            new_message = Message.objects.create(sender=sender, content=content)
            print("works")
    return render(request, 'test_chat.html')