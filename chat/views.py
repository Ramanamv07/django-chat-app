from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def checkview(request):
    room_name = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room_name).exists():
        return redirect('/'+room_name+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        return redirect('/'+room_name+'/?username='+username)
    
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {'room': room, 'room_details': room_details, 'username': username})

def send(request):
    username = request.POST['username']
    message = request.POST['message']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, username=username, room_id=room_id)
    new_message.save()
    return HttpResponse('Message Sent Successfully')

def getmessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room_id=room_details.id)
    return JsonResponse({'messages': list(messages.values())})