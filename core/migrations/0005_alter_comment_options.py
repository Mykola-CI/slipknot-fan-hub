# Generated by Django 5.0.4 on 2024-05-28 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_body_comment_content_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_on']},
        ),
    ]
