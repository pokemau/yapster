from django.urls import path
from . import views

app_name = "friend"

urlpatterns = [
    path('friends_list/<int:user_id>', views.friends_list_view, name='friends_list'),
    path('friend_request/<int:receiver_id>', views.send_friend_request, name='friend_request'),
    path('friend_requests', views.friend_requests_view, name='friend_requests'),
    path('accept_friend_request/<int:request_id>', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>', views.decline_friend_request, name='decline_friend_request'),
    path('remove_friend/<int:target_id>', views.remove_friend, name='remove_friend'),
]