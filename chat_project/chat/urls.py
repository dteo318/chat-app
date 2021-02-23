from django.urls import path
from .views import join_chat_view, room_view, update_users_ajax

urlpatterns = [
    path('', join_chat_view, name='join_chat'),
    path('ajax/getUsers/', update_users_ajax, name="update_users"),
    path('<str:room_name>/', room_view, name='room')
]
