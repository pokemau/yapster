from django.urls import path
from . import views

app_name = "friend"

urlpatterns = [
    path('friends_list', views.friends_list_view, name='friends_list'),
    path('friend_request/<int:receiver_id>', views.send_friend_request, name='friend_request'),
    path('friend_requests', views.friend_requests_view, name='friend_requests'),
    path('accept_friend_request/<int:request_id>', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>', views.decline_friend_request, name='decline_friend_request'),
    path('cancel_friend_request/<int:receiver_id>', views.cancel_friend_request, name='cancel_friend_request'),
    path('remove_friend/<int:target_id>', views.remove_friend, name='remove_friend'),
    path('block_list', views.block_list_view, name='block_list'),
    path('block_user/<int:target_id>', views.block_user, name='block_user'),
    path('unblock_user/<int:target_id>', views.unblock_user, name='unblock_user'),
    
    path('search', views.search_user, name='search'),
]