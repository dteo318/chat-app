from django.shortcuts import render
from .models import Room, Connection
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
# docker run -p 6379:6379 -d redis:5 
def join_chat_view(request):
    return render(request, 'chat/join_chat.html')

def room_view(request, user_name, room_name):

    if Room.objects.filter(group_name=room_name).count() == 0:
        room_model = Room(group_name=room_name)
        room_model.save()
    else:
        room_model = Room.objects.get(group_name=room_name)

    if Connection.objects.filter(username=user_name, connected_to=room_model).count() == 0:
        connection_model = Connection.objects.create(
            username=user_name,
            connected_to=room_model
        )
    else:
        connection_model = Connection.objects.get(
            username=user_name,
            connected_to=room_model
        )

    room_connections = room_model.room_connection.all()

    context = {
        'room_name'   : room_name,
        'user'        : connection_model,
        'connections' : room_connections
    }
    return render(request, 'chat/room.html', context=context)

def update_users_ajax(request):
    room_name = request.GET.get('room')
    room_model = Room.objects.get(group_name=room_name)
    room_connections = room_model.room_connection.all()
    data = {'room_connections' : serializers.serialize('json', room_connections)}

    return JsonResponse(data)

def remove_user_ajax(request):
    room_name = request.GET.get('room')
    room_model = Room.objects.get(group_name=room_name)
    user_name = request.GET.get('user')
    connection_model = Connection.objects.get(username=user_name, connected_to=room_model)

    connection_model.delete()
    print("deleted user model")
    
    data = {'user_deleted' : user_name}

    return JsonResponse(data)