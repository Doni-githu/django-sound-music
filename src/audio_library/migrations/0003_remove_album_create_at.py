# Generated by Django 4.2.4 on 2023-08-19 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio_library', '0002_album_create_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='create_at',
        ),
    ]