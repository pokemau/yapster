from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from chat.models import Message, YapsterUser, Chat, ChatUser
from user.models import User
from friend.models import FriendRequest, FriendList, BlockList
from django.db.models import Count, Q
from django.http import JsonResponse, Http404
import json
from django.contrib.auth.decorators import login_required
from collections import defaultdict

# Helper function for shared logic
def get_chat_data(request, active_chat_id=None):
    """Retrieve common chat data shared by chat_view and message_view."""
    query = request.GET.get('search', '').strip()
    users = None
    chat_users_mapping = []
    active_chat_data = None  # Stores specific data about the active chat
    
    # Search for users if a query is provided
    if query:
        users = YapsterUser.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)
        ).exclude(id=request.user.yapsteruser.id)
    
    # Get all chats involving the logged-in user
    chat_ids = ChatUser.objects.filter(member=request.user.yapsteruser).values_list('chat_id', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids)

    for chat in chats:
        users_in_chat = ChatUser.objects.filter(chat=chat).select_related('member')
        user_ids = [cu.member.id for cu in users_in_chat]
        is_PM = len(user_ids) == 2
        nicknames_in_chat = ChatUser.objects.filter(chat=chat)
        nicknames = [
            f"{cu.nickname}" for cu in nicknames_in_chat
        ]

        current_user_chat_user = users_in_chat.get(member=request.user.yapsteruser)
        current_user_nickname = current_user_chat_user.nickname

        nicknames_without_curruser = [
            cu.nickname for cu in nicknames_in_chat if cu.member != request.user.yapsteruser
        ]

        # Generate dynamic display name for group chats without a chat_name
        display_name = chat.chat_name or ", ".join(nicknames_without_curruser)

        chat_data = {
            'chat_id': chat.id,
            'chat_name': display_name,
            'user_ids': user_ids,
            'is_PM': is_PM,
            'nicknames': nicknames,
            'current_user_nickname': current_user_nickname,
            'nicknames_without_curruser': nicknames_without_curruser,
        }

        chat_users_mapping.append(chat_data)

        print(f"Checking chat: {chat.id}, active_chat_id: {active_chat_id}")

        # Fix: Explicitly compare with active_chat_id as an integer
        if active_chat_id and int(chat.id) == int(active_chat_id):
            active_chat_data = {
                'chat_room': chat,
                'display_name': display_name,
                'chat_users': users_in_chat,
                'is_pm': is_PM,
            }

    return query, users, chat_users_mapping, active_chat_data

# Updated chat_view
def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    query, users, chat_users_mapping, _ = get_chat_data(request)

    # Redirect to the latest chat if available
    if chat_users_mapping:
        latest_chat_id = chat_users_mapping[0]['chat_id']  # Use the first chat as a fallback
        return redirect('chat_name', chat_id=latest_chat_id)
    
    # If no chats, show a default view
    return render(request, 'chat.html', {
        'users': users,
        'query': query,
        'chat_users_mapping': chat_users_mapping,
        'current_userID': request.user.yapsteruser.id,
        'content': [],  # Empty content for new users
        'chat_room_users': [],  # No users in a new chat
    })

# Updated message_view
def message_view(request, chat_id):
    if not request.user.is_authenticated:
        return redirect('login')

    # Retrieve chat data, including active chat details
    query, users, chat_users_mapping, active_chat_data = get_chat_data(request, active_chat_id=chat_id)

    if not active_chat_data:
        raise Http404(f"Chat with id {chat_id} not found or not accessible.")

    chat_room = active_chat_data['chat_room']
    chat_users = active_chat_data['chat_users']

    # Determine the display name for the chat
    if active_chat_data['is_pm']:
        # For PM, display the other user's first and last name
        chat_users_without_current = [cu for cu in chat_users if cu.member != request.user.yapsteruser]
        if chat_users_without_current:
            # display_name = f"{chat_users_without_current[0].member.user.first_name} {chat_users_without_current[0].member.user.last_name}"
            display_name = chat_users_without_current[0].nickname
        else:
            display_name = "Unknown User"
    else:
        # For group chats, use the provided display name
        display_name = active_chat_data['display_name']

    messages = Message.objects.filter(chat=chat_room)
    content_messages = []
    last_sender = None

    senders = []
    counter = 0
    for message in messages:
        senders.append(message.sender)
    withPfp = [0] * len(senders)
    for i in range(len(senders) - 1, -1, -1):
        if i == len(senders) - 1 or senders[i] != senders[i + 1]:
            withPfp[i] = 1
    for message in messages:
        content_messages.append({
            'sender': message.sender,
            'message': message.content,
            'is_new_sender': last_sender != message.sender,
            'has_pfp': withPfp[counter] == 1,
            'system_message': message.system_message
        })
        print("SYTSTEM MESSAGE: ", message.system_message)
        last_sender = message.sender
        counter += 1
    
    pm_username = None
    chat_users_without_current = None
    if active_chat_data['is_pm']:
        chat_users_without_current = [cu for cu in active_chat_data['chat_users'] if cu.member != request.user.yapsteruser]
    if chat_users_without_current:
        pm_username = chat_users_without_current[0].member.user.username

    chat_users_id = [cu.member.user.id for cu in chat_users]
    # for i in chat_users:
    #     print("INVOLVED USER: ", i.nickname)
    #     print("ID: ", i.member.user.id)

    return render(request, 'chat.html', {
        'users': users,
        'query': query,
        'chat_users_mapping': chat_users_mapping,
        'current_userID': request.user.yapsteruser.id,
        'content': content_messages,
        'chat_room': chat_room,
        'chat_room_users_id': chat_users_id,
        'display_name': display_name,
        'is_pm': active_chat_data['is_pm'],
        'pm_username': pm_username,

    })

def query_users(request):
    if request.method == "GET":
        query = request.GET.get('gc_query', '').strip()
        if query:
            # Search for users
            users = YapsterUser.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__username__icontains=query)
            ).exclude(id=request.user.yapsteruser.id)

            # Search for group chats involving the logged-in user and the queried user(s)
            user_ids = YapsterUser.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__username__icontains=query)
            ).values_list('id', flat=True)

            group_chats = Chat.objects.filter(
                is_pm=False,
                chatuser__member=request.user.yapsteruser
            ).filter(
                chatuser__member_id__in=user_ids
            ).distinct()

            # Serialize users
            users_data = [
                {
                    'id': user.id,
                    'username': user.user.username,
                    'first_name': user.user.first_name,
                    'last_name': user.user.last_name,
                }
                for user in users
            ]

            # Serialize group chats
            chats_data = []
            for chat in group_chats:
                # Generate display name for unnamed group chats
                if not chat.chat_name:
                    nicknames = [
                        cu.nickname for cu in chat.chatuser.exclude(member=request.user.yapsteruser)
                    ]
                    display_name = ", ".join(nicknames)
                else:
                    display_name = chat.chat_name

                chats_data.append({
                    'chat_id': chat.id,
                    'chat_name': display_name,
                    'member_count': chat.chatuser.count(),
                })

            return JsonResponse({"users": users_data, "group_chats": chats_data})

        return JsonResponse({"success": False, "error": "No query provided"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

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

            try:
                other_user_block_list = BlockList.objects.get(user=user_profile)
                you_are_blocked = other_user_block_list.blocked_users.filter(id=request.user.yapsteruser.id).exists()
            except BlockList.DoesNotExist:
                you_are_blocked = False

            data = {
                'success': True,
                'id': user_profile.user.id,
                'first_name': user_profile.user.first_name,
                'username': user_profile.user.username,
                'bio': user_profile.bio,
                'friend_request_active': friend_request_exists,
                'is_friend': is_friend,
                'is_blocked': is_blocked,
                'you_are_blocked': you_are_blocked
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
        if(sender_id not in user_ids):
            user_ids.append(sender_id)
        print("USER IDSSSSSSSSS: ", user_ids)

        chat = find_chat(user_ids)

        if not chat:
            if len(user_ids) > 2:
                chat = Chat.objects.create(is_pm = False)
            else:    
                chat = Chat.objects.create()
            for user_id in user_ids:
                user = YapsterUser.objects.get(id=user_id)
                ChatUser.objects.create(chat=chat, member=user)

            if len(user_ids) <= 2:
                chat.chat_name = chat.id
            chat.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "chat_name": chat.id})
        
        #chat id siguro ni dapat
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

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Chat, ChatUser, YapsterUser, Message
import json

def add_members_to_group(request, chat_id):
    """Add members to a group chat."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

    # Get the chat object
    chat = get_object_or_404(Chat, id=chat_id)

    # Ensure that it's a group chat (not a PM)
    if chat.is_pm:
        return JsonResponse({"success": False, "error": "Cannot add members to a private message chat"}, status=400)

    if request.method == "POST":
        # Get the list of user IDs to add
        user_ids = request.POST.get('user_ids') or json.loads(request.body).get('user_ids')

        if not user_ids:
            return JsonResponse({"success": False, "error": "No users provided"}, status=400)

        # Filter out users who are already in the group chat
        existing_users = ChatUser.objects.filter(chat=chat, member__id__in=user_ids)
        existing_user_ids = [user.member.id for user in existing_users]

        # Check if any user is already in the group
        new_user_ids = [int(user_id) for user_id in user_ids if int(user_id) not in existing_user_ids]

        if not new_user_ids:
            return JsonResponse({"success": False, "error": "All users are already in the group."}, status=400)

        # Add new users to the chat
        for user_id in new_user_ids:
            user = get_object_or_404(YapsterUser, id=user_id)
            ChatUser.objects.create(chat=chat, member=user)

        # Create the system message about the added members
        added_users = ", ".join([f"{user.user.first_name} {user.user.last_name}" for user in YapsterUser.objects.filter(id__in=new_user_ids)])
      
        # Create a system message for the chat
        Message.objects.create(
            chat=chat,
            sender=request.user,
            content=f"{request.user.username} added {added_users}",
            system_message=True,
        )

        # Return a success response
        return JsonResponse({"success": True, "message": "Members added successfully!"})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

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