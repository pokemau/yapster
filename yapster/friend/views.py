from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from user.models import YapsterUser
from friend.models import FriendList, FriendRequest, BlockList
from .utils import get_friends_list, get_blocked_list
from django.db.models import Q
from django.http import JsonResponse

@login_required
def search_user_view(request):
    return render(request, 'search_user.html', {})

def friends_list_view(request):
    friend_list, created = FriendList.objects.get_or_create(user=request.user.yapsteruser)
    return render(request, 'friends_list.html', {'friend_list': friend_list.friends.all()})

@login_required
def friend_requests_view(request):
    requests = FriendRequest.objects.filter(receiver=request.user.yapsteruser, is_active=True)
    return render(request, 'friend_requests.html', {'friend_requests': requests})

@login_required
def send_friend_request(request, receiver_id):
    sender = request.user.yapsteruser
    receiver = YapsterUser.objects.get(user=receiver_id)

    friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver)

    if not friend_requests:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
    else:
        for req in friend_requests:
            if not req.is_active:
                req.is_active = True
                req.save()
    return redirect('chat')

@login_required
def cancel_friend_request(request, receiver_id):
    sender = request.user.yapsteruser
    receiver = YapsterUser.objects.get(user=receiver_id)
    friend_request = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)
    friend_request.cancel()
    return redirect('chat')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user.yapsteruser)
    receiver_friend_list, _ = FriendList.objects.get_or_create(user=request.user.yapsteruser)
    sender_friend_list, _ = FriendList.objects.get_or_create(user=friend_request.sender)

    print('=======')
    print('=======')
    print(type(friend_request))
    friend_request.accept()
    return redirect('friend:friend_requests')

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user.yapsteruser)
    friend_request.decline()
    return redirect('friend:friend_requests')

@login_required
def remove_friend(request, target_id):
    current_user = request.user.yapsteruser
    friend_list = get_friends_list(current_user)
    target_user = get_object_or_404(YapsterUser, user__id=target_id)
    friend_list.unfriend(target_user)
    return redirect('chat')

def block_list_view(request):
    blocked_list, created = BlockList.objects.get_or_create(user=request.user.yapsteruser)
    return render(request, 'block_list.html', {'blocked_list': blocked_list.blocked_users.all()})

@login_required
def block_user(request, target_id):
    current_user = request.user.yapsteruser
    block_list = BlockList.objects.get(user=current_user)
    target_user = get_object_or_404(YapsterUser, user__id=target_id)
    FriendRequest.objects.filter(
        (Q(sender=current_user) & Q(receiver=target_user)) |
        (Q(sender=target_user) & Q(receiver=current_user)),
        is_active=True
    ).update(is_active=False)
    friend_list, created = FriendList.objects.get_or_create(user=current_user)
    block_list.blocked_users.add(target_user)
    friend_list.unfriend(target_user)
    return redirect('chat')

@login_required
def unblock_user(request, target_id):
    current_user = request.user.yapsteruser
    block_list = BlockList.objects.get(user=current_user)
    target_user = get_object_or_404(YapsterUser, user__id=target_id)
    block_list.remove_from_block_list(target_user)
    return redirect('chat')

def search_user(request):
    query = request.GET.get('search', '')
    users = YapsterUser.objects.none()

    data = []

    if not query:
        return render(request, 'search_user.html')
    
    users = YapsterUser.objects.filter(
        (Q(user__first_name__icontains=query) |
         Q(user__last_name__icontains=query) |
         Q(user__username__icontains=query))
    ).exclude(id=request.user.yapsteruser.id)

    for user in users:
        try:
            other_user_block_list = BlockList.objects.get(user=user)
            you_are_blocked = other_user_block_list.blocked_users.filter(id=request.user.yapsteruser.id).exists()
        except BlockList.DoesNotExist:
            you_are_blocked = False
        if you_are_blocked:
            continue

        is_friend = FriendList.objects.filter(
            user=request.user.yapsteruser,
            friends=user
        ).exists()

        block_list, created = BlockList.objects.get_or_create(user=request.user.yapsteruser)
        is_blocked = BlockList.objects.filter(
            user=request.user.yapsteruser,
            blocked_users=user
        ).exists()

        friend_request_exists = FriendRequest.objects.filter(
                sender=request.user.yapsteruser,
                receiver=user,
                is_active=True
        ).exists()

        user_friend_request= FriendRequest.objects.filter(
                sender=user,
                receiver=request.user.yapsteruser,
                is_active=True
        ).first()



        data.append({
            'id': user.user.id,
            'first_name': user.user.first_name,
            'last_name': user.user.last_name,
            'profile_image': user.profile_image,
            'friend_request_exists': friend_request_exists,
            'user_friend_request': {
                'exists': user_friend_request,
                'id': user_friend_request.id if user_friend_request else None
            },
            'user_friend_request_exists': {

            },
            'is_friend': is_friend,
            'is_blocked': is_blocked,
        })
    return render(request, 'search_user.html', {'users': data})
