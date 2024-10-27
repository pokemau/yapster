from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from chat.models import Message, YapsterUser, Chat
from user.models import User

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'chat.html')

def logout_user(request):
    logout(request)
    return redirect('login')

# Handled in consumer for real time
# GWAAAAAPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPA
# SLAMM IBOG SHANLEY!
def test_chat_view(request):
    if request.method == "POST":
        chat_name = request.POST.get('chat')

        # Check if the chat already exists
        chat, created = Chat.objects.get_or_create(chat_name=chat_name)

        # Redirect to the message view with the username and chat_name
        username = request.user.username
        return redirect('chat_name', username, chat.chat_name)

    return render(request, 'test_chat_selector.html')

def message_view(request, username, chat_name):
    chat_room = Chat.objects.get(chat_name=chat_name)
    content_messages = Message.objects.filter(chat=chat_room)
    content = {
        "chat_room": chat_room,
        "content": content_messages,
        "sender" : username
    }
    print(content)
    return render(request, 'test_chat.html', content)