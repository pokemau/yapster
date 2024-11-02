from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from user.models import YapsterUser
from friend.models import FriendList, FriendRequest, BlockList
from .utils import get_friends_list, get_blocked_list

def friends_list_view(request, user_id):
    current_user = get_object_or_404(YapsterUser, user__id=user_id)
    friend_list, created = FriendList.objects.get_or_create(user=current_user)
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
    return redirect('friend:friends_list', user_id=request.user.id)

def block_list_view(request):
    return redirect('chat')

@login_required
def block_user(request, target_id):
    current_user = request.user.yapsteruser

    friend_list = get_friends_list(current_user)
    block_list = BlockList.objects.get(user=current_user)
    friend_request = get_object_or_404(FriendRequest, sender=current_user,
                                       receiver=YapsterUser.objects.get(user=target_id))
    friend_request.cancel()
    target_user = get_object_or_404(YapsterUser, user__id=target_id)
    block_list.add_to_block_list(target_user)
    friend_list.unfriend(target_user)
    return redirect('chat')

@login_required
def unblock_user(request, target_id):
    current_user = request.user.yapsteruser
    block_list = BlockList.objects.get(user=current_user)
    target_user = get_object_or_404(YapsterUser, user__id=target_id)
    block_list.remove_from_block_list(target_user)
    return redirect('chat')