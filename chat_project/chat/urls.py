from django.urls import path
from .views import join_chat_view, room_view

urlpatterns = [
    path('', join_chat_view, name='join_chat'),
    path('<str:user_name>/<str:room_name>/', room_view, name='room')
]
