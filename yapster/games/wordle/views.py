from django.shortcuts import render, redirect
from .models import WordleGame
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json


def wordle_view(request, game_id):
    game = WordleGame.objects.get(id=game_id)
    return render(request, 'wordle.html', {'game': game})

@login_required
@csrf_exempt
def create_wordle_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word = data.get('word')
            
            wordle_game = WordleGame.objects.create(
                creator=request.user.yapsteruser,
                word=word
            )

            return JsonResponse({
                'success': True, 
                'game': wordle_game.id
            })

        except Exception as e:
            print(f"EXCEPTION {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False})
