# Generated by Django 5.0.6 on 2024-06-12 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_likedanime',
            old_name='liked_anime',
            new_name='anime',
        ),
        migrations.RenameField(
            model_name='user_likedanime',
            old_name='email',
            new_name='user',
        ),
    ]