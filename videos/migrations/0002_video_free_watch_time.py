# Generated by Django 5.1.4 on 2024-12-29 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='free_watch_time',
            field=models.DurationField(default=datetime.timedelta(seconds=4)),
        ),
    ]