from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('logout/', views.logout_user, name='logout'),
    
    path('user-details/<int:user_id>/', views.get_user_details, name="user_details"),
    path('get_or_create_chat/', views.get_or_create_chat, name="get_or_create_chat"),
    path('<str:chat_id>/', views.message_view, name='chat_name'),
    path('query_stuff/query_users/', views.query_users, name="query_users"),

    # path('search/', views.search_user, name='search_user'),
    # path('temp/<int:user_id>/', views.temp_chat_view, name="temp_chat"),
]