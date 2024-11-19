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
    
    users = YapsterUser.objects.exclude(id=request.user.yapsteruser.id)
    
    return render(request, 'chat.html', {'users': users})

def logout_user(request):
    logout(request)
    return redirect('login')

def search_user(request):
    query = request.GET.get('search', '')
    users = YapsterUser.objects.none()

    if not query:
        return render(request, 'chat.html')
    
    print("Test: " + str(users))
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
        return redirect('chat_name', chat.chat_name)

    return render(request, 'test_chat_selector.html')

#Temp Chat for chatting unchatted user
def temp_chat_view(request, user_id):
    target_user = get_object_or_404(YapsterUser, id=user_id)
    return render(request, 'chat.html', {'target_user': target_user, 'is_temp': True})
    
def get_or_create_chat(request):
    if request.method == "POST":
        target_user_id = request.POST.get('target_user_id')  # Sent from the form
        message_content = request.POST.get('message')  # The first message

        # Get the sender and target user
        sender = request.user.username
        target_user = get_object_or_404(YapsterUser, id=target_user_id)

        # Check if a chat already exists
        # chat, created = Chat.objects.get_or_create(participants__in=[sender, target_user])

        # Check if a chat already exists between the users
        # chat = Chat.objects.filter(participants=sender).filter(participants=target_user).first()

        # if not chat:
            # Create a new chat
        chat = Chat.objects.create() # Generates an Id
        chat.chat_name = chat.id  # Use any naming format you prefer
        chat.save()

        # Save the message
        if message_content:
            Message.objects.create(chat=chat, sender=request.user, content=message_content)

        # Redirect to the proper chat room
        return redirect('chat_name', chat_name=chat.id)

def message_view(request, chat_name):
    chat_room = Chat.objects.get(chat_name=chat_name)
    content_messages = Message.objects.filter(chat=chat_room)
    content = {
        "chat_room": chat_room,
        "content": content_messages,
        "sender" : request.user.username
    }
    print(content)
    return render(request, 'chat.html', content)