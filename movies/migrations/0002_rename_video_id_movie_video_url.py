# Generated by Django 3.2.9 on 2021-11-18 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='video_id',
            new_name='video_url',
        ),
    ]
