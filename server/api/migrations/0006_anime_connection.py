# Generated by Django 5.0.6 on 2024-05-27 23:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_anime_connection'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='connection',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='liked_anime', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]