from django.urls import path
from . import views

app_name = 'wordle'

urlpatterns = [
    path('', views.wordle_view, name='wordle_main'),
    path('<int:game_id>', views.wordle_view, name='wordle_main'),
    path('create_game', views.create_wordle_game, name='create_wordle_game'),
    path('update_game/<int:game_id>', views.update_game, name='update_wordle_game')
]