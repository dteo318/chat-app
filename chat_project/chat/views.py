from django.shortcuts import render
from .models import Room, Connection
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
# docker run -p 6379:6379 -d redis:5 
def join_chat_view(request):
    return render(request, 'chat/join_chat.html')

def room_view(request, room_name):
    return render(request, 'chat/room.html', {'room_name' : room_name})

def update_users_ajax(request):
    room_name = request.GET.get('room')
    room_model = Room.objects.get(group_name=room_name)
    room_connections = room_model.room_connection.all()
    data = {'room_connections' : serializers.serialize('json', room_connections)}

    return JsonResponse(data)

def set_room_password_ajax(request):
    room_name = request.GET.get('room')
    room_model = Room.objects.get(group_name=room_name)
    password = request.GET.get('password')
    room_model.password = password
    room_model.save(update_fields=["password"])
    return JsonResponse({})

def check_room_password_ajax(request):
    room_name = request.GET.get('room')
    room_model = Room.objects.get(group_name=room_name)
    password = request.GET.get('password')
    return JsonResponse({
       'is_correct_password' : room_model.password == password
    })