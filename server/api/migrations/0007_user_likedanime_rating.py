# Generated by Django 5.0.7 on 2024-07-18 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_anime_genres_alter_anime_studios'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_likedanime',
            name='rating',
            field=models.FloatField(null=True),
        ),
    ]