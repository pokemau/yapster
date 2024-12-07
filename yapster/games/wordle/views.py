from django.shortcuts import render, redirect, get_object_or_404
from .models import WordleGame
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from chat.models import Chat


def wordle_view(request, game_id):
    try:
        game = WordleGame.objects.get(id=game_id)
        return render(request, 'wordle.html', {'game': game})
    except WordleGame.DoesNotExist:
        return redirect('chat')

@login_required
@csrf_exempt
def create_wordle_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word = data.get('word')
            room = data.get('room')
            chat = get_object_or_404(Chat, id=room)
            
            wordle_game = WordleGame.objects.create(
                creator=request.user.yapsteruser,
                chatroom=chat,
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

def update_game(request, game_id):
    if request.method == 'POST':
        try:
            print("TRY")
            data = json.loads(request.body)
            guesses = data.get('guesses')

            game_obj = WordleGame.objects.get(id=game_id)
            game_obj.guesses = guesses
            game_obj.tries = len(str(guesses).split(','))
            game_obj.solved = True
            game_obj.save()

            return JsonResponse({
                'success': True
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False})