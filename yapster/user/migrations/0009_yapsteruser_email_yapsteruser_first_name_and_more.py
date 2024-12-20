# Generated by Django 5.1.2 on 2024-11-17 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_yapsteruser_cover_photo_alter_yapsteruser_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='yapsteruser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='yapsteruser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='yapsteruser',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
