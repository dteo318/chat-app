from django.urls import path
from .views import join_chat_view, room_view, update_users_ajax, set_room_password_ajax, check_room_password_ajax

urlpatterns = [
    path('', join_chat_view, name='join_chat'),
    path('ajax/getUsers/', update_users_ajax, name="update_users"),
    path('ajax/SetPassword/', set_room_password_ajax, name="set_room_password"),
    path('ajax/checkPassword/', check_room_password_ajax, name="check_room_password"),
    path('<str:room_name>/', room_view, name='room')
]
