# Generated by Django 5.0.4 on 2024-06-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_playlistpost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistpost',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
