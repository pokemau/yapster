# Generated by Django 5.1.1 on 2024-12-10 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_message_system_message_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='is_pm',
            field=models.BooleanField(default=True),
        ),
    ]