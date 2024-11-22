from django.urls import path
from . import views

app_name = 'wordle'

urlpatterns = [
    path('', views.wordle_view, name='wordle_main'),
    path('<int:game_id>', views.wordle_view, name='wordle_main'),
]