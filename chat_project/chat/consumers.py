import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Connection, Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.username = self.scope['url_route']['kwargs']['username']
        # Join room group

        await database_sync_to_async(self.connect_user)(self.username, self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await database_sync_to_async(self.disconnect_user)(self.username, self.room_name)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        current_user = text_data_json['username']
        message = text_data_json['message']
        message_type = text_data_json['message_type']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': message_type,
                'username' : current_user,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        current_user = event['username']
        message_type = event['message_type']

        if message_type == 'save_message':
            await database_sync_to_async(self.save_message)(current_user, self.room_name, message)
            print("CREATE SAVED MESSAGE")
            
        elif message_type == 'unsave_message':
            await database_sync_to_async(self.unsave_message)(current_user, self.room_name, message)
            print("DELETE SAVED MESSAGE")
        else:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message_type': message_type,
                'message': message,
                'username' : current_user
            }))

    def disconnect_user(self, user_name, room_name):
        room_model = Room.objects.get(group_name=room_name)
        connection_model = Connection.objects.get(username=user_name, connected_to=room_model)
        connection_model.delete()

    def connect_user(self, user_name, room_name):
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

    def save_message(self, user_name, room_name, selected_message):
        room_model = Room.objects.get(group_name=room_name)
        connection_model = Connection.objects.get(username=user_name, connected_to=room_model)
        message_model = Message.objects.create(
            sent_by = connection_model,
            sent_in_room = room_model,
            saved_message = selected_message
        )
    
    def unsave_message(self, user_name, room_name, selected_message):
        room_model = Room.objects.get(group_name=room_name)
        connection_model = Connection.objects.get(username=user_name, connected_to=room_model)
        message_model = Message.objects.get(
            sent_by = connection_model,
            sent_in_room = room_model,
            saved_message = selected_message
        )
        
        message_model.delete()