from django.shortcuts import render
from user.models import YapsterUser

def friends_list_view(request, *args, **kwargs):
    return render(request, 'friends_list.html')
