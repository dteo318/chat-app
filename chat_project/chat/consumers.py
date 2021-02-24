import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Connection, Message
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core import serializers

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

        room_messages = await database_sync_to_async(self.get_room_messages)(self.room_name)

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_type': 'display_saved_messages',
            'messages': await sync_to_async(serializers.serialize)('json', room_messages)
        }))

        password = await database_sync_to_async(self.get_password)(self.room_name)

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_type': 'update_password',
            'message': password
        }))

    async def disconnect(self, close_code):
        await database_sync_to_async(self.disconnect_user)(self.username, self.room_name)

        # Closes room on all connections closed - Will loose message data
        # room_is_empty = await database_sync_to_async(self.no_more_connections)(self.room_name)

        # if room_is_empty:
        #     await database_sync_to_async(self.delete_room)(self.room_name)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']

        if message_type == 'update_password':
            password = text_data_json['password']
            await database_sync_to_async(self.update_room_password)(self.room_name, password)
            print("PASSWORD UPDATED")
            # Send new password to all channels
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_type': "update_password",
                    'message': password
                }
            )

        else:
            current_user = text_data_json['username']
            message = text_data_json['message']

            if message_type == 'save_message':
                await database_sync_to_async(self.save_message)(current_user, self.room_name, message)
                print("CREATE SAVED MESSAGE")
                
            elif message_type == 'unsave_message':
                await database_sync_to_async(self.unsave_message)(current_user, self.room_name, message)
                print("DELETE SAVED MESSAGE")
                
            else:
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
        # Send message to WebSocket
        message_type = event['message_type']

        if message_type == 'update_password':
            message = event['message']
            await self.send(text_data=json.dumps({
                    'message_type': message_type,
                    'message': message,
                }))
        else:
            message = event['message']
            current_user = event['username']
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
        message_model = Message.objects.create(
            sent_by = user_name,
            sent_in_room = room_model,
            saved_message = selected_message
        )
    
    def unsave_message(self, user_name, room_name, selected_message):
        room_model = Room.objects.get(group_name=room_name)
        message_model = Message.objects.get(
            sent_by = user_name,
            sent_in_room = room_model,
            saved_message = selected_message
        )
        
        message_model.delete()

    def get_room_messages(self, room_name):
        room_model = Room.objects.get(group_name=room_name)
        room_messages = room_model.room_message.all().order_by("-sent_date")
        return room_messages

    def no_more_connections(self, room_name):
        return Room.objects.get(group_name=room_name).room_connection.count() == 0

    def delete_room(self, room_name):
        room_model = Room.objects.get(group_name=room_name)
        room_model.delete()

    def update_room_password(self, room_name, password):
        room_model = Room.objects.get(group_name=room_name)
        room_model.password = password
        room_model.save(update_fields=['password'])

    def get_password(self, room_name):
        room_model = Room.objects.get(group_name=room_name)
        return room_model.password