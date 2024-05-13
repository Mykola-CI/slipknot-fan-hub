# Generated by Django 5.0.4 on 2024-05-09 15:11

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_avatar', max_length=255, verbose_name='image'),
        ),
    ]