# Generated by Django 5.1.1 on 2024-10-27 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_chatuser_member_alter_message_sender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatuser',
            old_name='chat_belong',
            new_name='chat',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='chat_belong',
            new_name='chat',
        ),
        migrations.AlterField(
            model_name='chat',
            name='chat_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
