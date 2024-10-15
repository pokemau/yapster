from django.shortcuts import render
from chat.models import Message, YapsterUser
from user.models import User

def chat_view(request):
    return render(request, 'chat.html')

def test_chat_view(request):
    # check if logged in need verify na login si user
    # need nay chat na na belong (pwede default chat)
    if request.method=="POST":
        content = request.POST["message_to_send"]
        if 'logged_user' in request.session:
            sender = User.objects.get(id=request.session['logged_user'])
            new_message = Message.objects.create(sender=sender, content=content)
    return render(request, 'test_chat.html')