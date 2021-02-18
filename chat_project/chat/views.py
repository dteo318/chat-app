from django.shortcuts import render

# Create your views here.
# docker run -p 6379:6379 -d redis:5 
def join_chat_view(request):
    return render(request, 'chat/join_chat.html')

def room_view(request, room_name):
    return render(request, 'chat/room.html', {'room_name':room_name})