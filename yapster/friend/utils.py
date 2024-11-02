from .models import FriendList, YapsterUser

def get_friends_list(user: YapsterUser):
    return FriendList.objects.get(user=user)
    
def get_blocked_list(user: YapsterUser):
    pass