from django.shortcuts import render
from .models import Room, Connection
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

    return render(request, 'chat/room.html', {'room_name':room_name})