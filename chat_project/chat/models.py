from django.db import models

# Create your models here.
class Room(models.Model):
    group_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.group_name

class Connection(models.Model):
    username = models.CharField(max_length=200)
    connected_to = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_connection")

    def __str__(self):
        return self.username

class Message(models.Model):
    sent_by = models.ForeignKey(Connection, on_delete=models.CASCADE, related_name="connection_message")
    sent_in_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_message")
    sent_date = models.DateTimeField(auto_now_add=True)
    saved_message = models.CharField(max_length=500, default="")