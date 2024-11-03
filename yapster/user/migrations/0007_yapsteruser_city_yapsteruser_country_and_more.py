# Generated by Django 5.1.1 on 2024-11-02 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_yapsteruser_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='yapsteruser',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yapsteruser',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yapsteruser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='yapsteruser',
            name='postcode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='yapsteruser',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
