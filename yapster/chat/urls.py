from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('logout/', views.logout_user, name='logout'),
    
    path('test_chat_selector/', views.test_chat_view, name='test_chat_selector'),
    path('<str:username>/<str:chat_name>/', views.message_view, name='chat_name'),
]