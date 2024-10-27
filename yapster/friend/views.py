from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from user.models import YapsterUser
from friend.models import FriendList, FriendRequest

def friends_list_view(request, user_id):
    current_user = get_object_or_404(YapsterUser, user__id=user_id)
    friend_list, created = FriendList.objects.get_or_create(user=current_user)
    print(f'friend list {friend_list}')
    if created:
        print("CREATED NEW FRIEND LIST TABLE")
    return render(request, 'friends_list.html', {'friend_list': friend_list.friends.all()})

@login_required
def friend_requests_view(request):
    print(f'getting friend requests for user {request.user.yapsteruser}')
    requests = FriendRequest.objects.filter(receiver=request.user.yapsteruser, is_active=True)
    print(f'requests: {requests}')
    return render(request, 'friend_requests.html', {'friend_requests': requests})

@login_required
def send_friend_request(request, receiver_id):
    sender = request.user.yapsteruser
    receiver = YapsterUser.objects.get(user=receiver_id)

    friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver)

    if not friend_requests:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        print("SENT A FRIEND REQUEST")
    else:
        for req in friend_requests:
            if not req.is_active:
                req.is_active = True
                req.save()
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
    friend_list = FriendList.objects.get(user=current_user)
    target_user = get_object_or_404(YapsterUser, user__id=target_id)
    friend_list.unfriend(target_user)
    return redirect('friend:friends_list', user_id=request.user.id)
