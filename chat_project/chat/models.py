from django.db import models

# Create your models here.
class Room(models.Model):
    group_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200, null=True)

class Connection(models.Model):
    username = models.CharField(max_length=200)
    connected_to = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_connection")
