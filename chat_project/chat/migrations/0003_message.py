# Generated by Django 3.1.6 on 2021-02-23 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_room_have_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection_message', to='chat.connection')),
                ('sent_in_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_message', to='chat.room')),
            ],
        ),
    ]