from django.shortcuts import render
from .models import WordleGame


def wordle_view(request, game_id):
    game = WordleGame.objects.get(id=game_id)
    print(f"THE WORD IS {game.word}")
    return render(request, 'wordle.html', {})
    