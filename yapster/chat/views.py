from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from chat.models import Message, YapsterUser, Chat
from user.models import User
from friend.models import FriendRequest, FriendList, BlockList
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'chat.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def search_user(request):
    query = request.GET.get('search', '')
    users = YapsterUser.objects.none()

    if not query:
        return render(request, 'chat.html')
    
    users = YapsterUser.objects.filter(
        (Q(user__first_name__icontains=query) |
         Q(user__last_name__icontains=query) |
         Q(user__username__icontains=query))
    ).exclude(id=request.user.yapsteruser.id)

    return render(request, 'chat.html', {'users': users, 'query': query})


def friends_list_view(request, user_id):
    current_user = get_object_or_404(YapsterUser, user__id=user_id)
    friend_list, created = FriendList.objects.get_or_create(user=current_user)
    return render(request, 'friends_list.html', {'friend_list': friend_list.friends.all()})

@login_required
def get_user_details(request, user_id):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            user_profile = YapsterUser.objects.select_related('user').get(id=user_id)
            friend_request_exists = FriendRequest.objects.filter(
                sender=request.user.yapsteruser,
                receiver=user_profile,
                is_active=True
            ).exists()
            
            is_friend = FriendList.objects.filter(
                user=request.user.yapsteruser,
                friends=user_profile
            ).exists()

            block_list, created = BlockList.objects.get_or_create(user=request.user.yapsteruser)
            is_blocked = BlockList.objects.filter(
                user=request.user.yapsteruser,
                blocked_users=user_profile
            ).exists()

            data = {
                'success': True,
                'id': user_profile.user.id,
                'first_name': user_profile.user.first_name,
                'username': user_profile.user.username,
                'bio': user_profile.bio,
                'friend_request_active': friend_request_exists,
                'is_friend': is_friend,
                'is_blocked': is_blocked
            }
            
            return JsonResponse(data)
        except YapsterUser.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


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