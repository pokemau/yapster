from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('landing/', views.landing_page_view, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('update/', views.update_user, name='update_user'),
    path('delete/', views.delete_user, name='delete_user'),
    path('profile/<int:user_id>/', views.profile_page, name='profile_page'),
    path('update_profile/<int:user_id>/', views.update_profile, name='update_profile'),
    path('public_profile/<int:user_id>/', views.public_profile, name='public_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('change_password/', views.change_password, name='change_password'),

]