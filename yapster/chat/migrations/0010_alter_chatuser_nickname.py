# yapster/chat/migrations/0010_alter_chatuser_nickname.py

from django.db import migrations, models

def set_default_nickname(apps, schema_editor):
    ChatUser = apps.get_model('chat', 'ChatUser')
    for chat_user in ChatUser.objects.filter(nickname__isnull=True):
        chat_user.nickname = 'default_nickname'
        chat_user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_chatuser_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatuser',
            name='nickname',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.RunPython(set_default_nickname),
        migrations.AlterField(
            model_name='chatuser',
            name='nickname',
            field=models.CharField(max_length=255, null=False),
        ),
    ]