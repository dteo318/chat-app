from django.shortcuts import render

# Create your views here.
def join_chat_view(request):
    return render(request, 'chat/join_chat.html')

def room_view(request, room_name):
    return render(request, 'chat/room.html', {'room_name':room_name})