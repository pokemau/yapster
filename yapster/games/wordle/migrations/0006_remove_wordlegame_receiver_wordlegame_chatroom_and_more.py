# Generated by Django 5.1.1 on 2024-12-06 02:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_alter_chatuser_nickname'),
        ('wordle', '0005_alter_wordlegame_creator_alter_wordlegame_receiver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordlegame',
            name='receiver',
        ),
        migrations.AddField(
            model_name='wordlegame',
            name='chatroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wordle_chatroom', to='chat.chat'),
        ),
        migrations.AddField(
            model_name='wordlegame',
            name='solved',
            field=models.BooleanField(default=False),
        ),
    ]
