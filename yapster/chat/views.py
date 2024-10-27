from django.shortcuts import render, redirect
from django.contrib.auth import logout
from chat.models import Message, YapsterUser
from user.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'chat.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def search_user(request):
    query = request.GET.get('search', '')
    users = YapsterUser.objects.none()

    if not query:
        return render(request, 'chat.html')
    
    users = YapsterUser.objects.filter(
        user__first_name__icontains=query
    ) | YapsterUser.objects.filter(
        user__last_name__icontains=query
    ) | YapsterUser.objects.filter(user__username__icontains=query)

    return render(request, 'chat.html', {'users': users, 'query': query})

@login_required
def get_user_details(request, user_id):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            user_profile = YapsterUser.objects.select_related('user').get(id=user_id)
            data = {
                'success': True,
                'id': user_profile.user.id,
                'first_name': user_profile.user.first_name,
                'username': user_profile.user.username,
                'bio': user_profile.bio,
            }
            return JsonResponse(data)
        except YapsterUser.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


def test_chat_view(request):
    # check if logged in need verify na login si user
    # need nay chat na na belong (pwede default chat)
    if request.method=="POST":
        content = request.POST["message_to_send"]
        if 'logged_user' in request.session:
            sender = User.objects.get(id=request.session['logged_user'])
            new_message = Message.objects.create(sender=sender, content=content)
            print("works")
    return render(request, 'test_chat.html')