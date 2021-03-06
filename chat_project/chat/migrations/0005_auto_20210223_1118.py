# Generated by Django 3.1.6 on 2021-02-23 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_saved_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='connection_message', to='chat.connection'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sent_in_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_message', to='chat.room'),
        ),
    ]
