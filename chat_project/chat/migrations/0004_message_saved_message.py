# Generated by Django 3.1.6 on 2021-02-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='saved_message',
            field=models.CharField(default='', max_length=500),
        ),
    ]