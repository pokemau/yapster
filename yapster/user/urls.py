from django.urls import path
from . import views
from .views import update_profile, view_public_profile

urlpatterns = [
    path('', views.index_view, name='index'),
    path('landing/', views.landing_page_view, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('update/', views.update_user, name='update_user'),
    path('delete/', views.delete_user, name='delete_user'),
    path('profile/', views.profile_page, name='profile_page'),
    path('update-profile/', update_profile, name='update_profile'),
    path('public-profile/', view_public_profile, name='public_profile'),
]