from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search_user, name='search_user'),
    path('user-details/<int:user_id>/', views.user_details_view, name="user_details"),
    path('test_chat/', views.test_chat_view, name='test_chat'),
]