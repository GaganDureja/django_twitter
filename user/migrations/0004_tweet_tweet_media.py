# Generated by Django 5.0.2 on 2024-02-14 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_t_media_user_verified_account_tweet_replytweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='tweet_media',
            field=models.ManyToManyField(to='user.t_media'),
        ),
    ]
