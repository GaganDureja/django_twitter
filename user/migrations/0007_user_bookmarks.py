# Generated by Django 5.0.2 on 2024-02-20 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bookmarks',
            field=models.ManyToManyField(related_name='my_bookmarks', to='user.tweet'),
        ),
    ]
