# Generated by Django 5.1.5 on 2025-01-30 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_subject_alter_video_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='embed_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
