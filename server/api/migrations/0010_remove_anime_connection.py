# Generated by Django 5.0.6 on 2024-05-28 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_anime_connection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='connection',
        ),
    ]
