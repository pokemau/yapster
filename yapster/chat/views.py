from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from chat.models import Message, YapsterUser, Chat, ChatUser
from user.models import User
from friend.models import FriendRequest, FriendList, BlockList
from django.db.models import Count, Q
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from collections import defaultdict

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    query = request.GET.get('search', '').strip()
    users = None
    chat_users_mapping = []

    if query:
        users = YapsterUser.objects.filter(
            (Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query))
        ).exclude(id=request.user.yapsteruser.id)
    else:
        # Get all chats involving the logged-in user
        chat_ids = ChatUser.objects.filter(member=request.user.yapsteruser).values_list('chat_id', flat=True)
        chats = Chat.objects.filter(id__in=chat_ids)

        # Build the chat_users_mapping
        for chat in chats:
            users_in_chat = ChatUser.objects.filter(chat=chat).select_related('member')
            user_ids = [cu.member.id for cu in users_in_chat]
            user_names = [
                f"{cu.member.user.first_name} {cu.member.user.last_name}" for cu in users_in_chat
            ]
            chat_users_mapping.append({
                'chat_id': chat.id,
                'chat_name': chat.chat_name,
                'user_ids': user_ids,
                'user_names': user_names,
            })
    
    return render(request, 'chat.html', {'users': users, 'query': query, 'chat_users_mapping' : chat_users_mapping})

def logout_user(request):
    logout(request)
    return redirect('login')

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

def get_or_create_chat(request):
    # Based on users involved
    if request.method == "POST":
        user_ids = request.POST.get('target_user_ids') or json.loads(request.body).get('target_user_ids')
        print("GAGAGAGAGAG")
        
        sender_id = request.user.yapsteruser.id
        user_ids.append(sender_id)
        print(user_ids)
        chat = find_chat(user_ids)

        if not chat:
            chat = Chat.objects.create()
            for user_id in user_ids:
                user = YapsterUser.objects.get(id=user_id)
                ChatUser.objects.create(chat=chat, member=user)

            chat.chat_name = chat.id
            chat.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "chat_name": chat.chat_name})
        
        return redirect('chat_name', chat_name=chat.chat_name)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def find_chat(user_ids):
    user_ids = list(map(int, user_ids))

    candidate_chats = Chat.objects.all()

    for user_id in user_ids:
        candidate_chats = candidate_chats.filter(chatuser__member_id=user_id)

    for chat in candidate_chats:
        participant_ids = set(chat.chatuser.values_list('member_id', flat=True))
        
        print("Participant IDS: ", participant_ids)
        print("USerid set: ", set(user_ids))

        if participant_ids == set(user_ids):
            return chat

    return None

def get_user_chats_with_id(request):
    pass

def message_view(request, chat_name):
    query = request.GET.get('search', '').strip()
    if query:
        users = YapsterUser.objects.filter(
            (Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query))
        ).exclude(id=request.user.yapsteruser.id)
    else:
        #Chat list here
        users = YapsterUser.objects.exclude(id=request.user.yapsteruser.id)

    chat_room = Chat.objects.get(chat_name=chat_name)
    content_messages = Message.objects.filter(chat=chat_room)
    content = {
        "chat_room": chat_room,
        "content": content_messages,
        "sender" : request.user.username,
        'users': users, 
        'query': query
    }
    print("CHAT: \n", chat_room)
    


    return render(request, 'chat.html', content)


#Temp Chat for chatting unchatted user
# def temp_chat_view(request, user_id):
#     target_user = get_object_or_404(YapsterUser, id=user_id)
#     return render(request, 'chat.html', {'target_user': target_user, 'is_temp': True})

# Handled in consumer for real time
# GWAAAAAPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPA
# SLAMM IBOG SHANLEY!
# def test_chat_view(request):
#     if request.method == "POST":
#         chat_name = request.POST.get('chat')

#         # Check if the chat already exists
#         chat, created = Chat.objects.get_or_create(chat_name=chat_name)

#         # Redirect to the message view with the username and chat_name
#         return redirect('chat_name', chat.chat_name)

#     return render(request, 'test_chat_selector.html')

# def get_or_create_chat(request):
#     if request.method == "POST":
#         target_user_id = request.POST.get('target_user_id')
        
#         user_ids = [target_user_id]
#         sender_id = request.user.yapsteruser.id
#         user_ids.append(sender_id)

#         for user_id in user_ids:
#             print("USER ID: ", user_id)
#         chat = find_chat(user_ids)

#         if not chat:
#             chat = Chat.objects.create()

#             for user_id in user_ids:
#                 user = YapsterUser.objects.get(id=user_id)
#                 ChatUser.objects.create(chat=chat, member=user)

#             chat.chat_name = f"Chat-{chat.id}"
#             chat.save()

#         return redirect('chat_name', chat_name=chat.chat_name)