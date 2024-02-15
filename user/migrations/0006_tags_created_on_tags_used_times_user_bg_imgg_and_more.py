# Generated by Django 5.0.2 on 2024-02-15 16:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tags',
            name='used_times',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='bg_imgg',
            field=models.FileField(blank=True, null=True, upload_to='profile'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_imgg',
            field=models.FileField(blank=True, null=True, upload_to='profile'),
        ),
    ]