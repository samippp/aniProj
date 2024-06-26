# Generated by Django 5.0.6 on 2024-06-15 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_likedanime_date_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_likedanime',
            name='id',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddConstraint(
            model_name='user_likedanime',
            constraint=models.UniqueConstraint(fields=('user', 'anime'), name='unique_favourite'),
        ),
    ]
