# Generated by Django 5.1.1 on 2024-12-07 00:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_alter_chat_is_pm'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='system_message',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]