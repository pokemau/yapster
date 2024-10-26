from django.urls import path
from . import views

app_name = "friend"

urlpatterns = [
    # path('', views.friends_list_view, name='friend_list'),
    path('friends_list/<user_id>/', views.friends_list_view, name='friends_list'),
]