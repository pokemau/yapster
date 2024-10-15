from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('test_chat/', views.test_chat_view, name='test_chat'),
]