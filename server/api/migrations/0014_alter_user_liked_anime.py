# Generated by Django 5.0.6 on 2024-05-29 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_user_email_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_anime',
            field=models.ManyToManyField(blank=True, to='api.anime'),
        ),
    ]