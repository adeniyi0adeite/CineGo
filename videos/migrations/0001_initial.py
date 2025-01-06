# Generated by Django 5.1.4 on 2025-01-04 17:23

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_file', models.FileField(upload_to='videos_uploads/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('genre', models.CharField(choices=[('action', 'Action'), ('drama', 'Drama'), ('comedy', 'Comedy'), ('horror', 'Horror'), ('thriller', 'Thriller')], max_length=50)),
                ('parental_guidance', models.CharField(choices=[('G', 'General Audience'), ('PG', 'Parental Guidance'), ('PG-13', 'Parents Strongly Cautioned'), ('R', 'Restricted'), ('NC-17', 'Adults Only')], max_length=10)),
                ('running_time', models.DurationField(default=datetime.timedelta(0))),
                ('premiere', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('artwork', models.ImageField(blank=True, null=True, upload_to='artworks/')),
                ('release_date', models.DateField(default=django.utils.timezone.now)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('actors', models.ManyToManyField(related_name='movies_set', to='users.actor')),
                ('categories', models.ManyToManyField(blank=True, related_name='videos', to='videos.category')),
                ('director', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='directed_videos', to='users.director')),
            ],
        ),
        migrations.CreateModel(
            name='VideoAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_granted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
        ),
    ]
