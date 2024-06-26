# Generated by Django 5.0.6 on 2024-06-12 23:16

import api.models
import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('desc', models.TextField()),
                ('studios', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=60), size=None)),
                ('genres', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=35), size=None)),
                ('popularity', models.IntegerField()),
                ('score', models.FloatField()),
                ('img', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', api.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='user_likedanime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_liked', models.DateField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('liked_anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.anime')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='liked_anime',
            field=models.ManyToManyField(blank=True, through='api.user_likedanime', to='api.anime'),
        ),
    ]
