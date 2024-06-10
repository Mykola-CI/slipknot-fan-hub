# Generated by Django 5.0.4 on 2024-06-10 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0009_alter_playlist_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='playlistitem',
            name='song_comments',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about_myself',
            field=models.CharField(blank=True, max_length=500, verbose_name='about myself'),
        ),
    ]
