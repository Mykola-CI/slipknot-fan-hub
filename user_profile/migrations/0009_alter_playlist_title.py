# Generated by Django 5.0.4 on 2024-06-06 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_remove_playlistitem_song_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]