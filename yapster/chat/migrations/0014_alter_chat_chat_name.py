# Generated by Django 5.1.1 on 2024-12-04 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_chat_chat_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='chat_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
