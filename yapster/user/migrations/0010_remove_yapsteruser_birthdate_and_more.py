# Generated by Django 5.1.1 on 2024-11-24 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_yapsteruser_email_yapsteruser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yapsteruser',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='yapsteruser',
            name='cover_photo',
        ),
    ]
