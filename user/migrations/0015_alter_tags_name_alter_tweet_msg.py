# Generated by Django 5.0.2 on 2024-02-22 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.TextField(db_collation='utf8mb4_unicode_ci', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='msg',
            field=models.TextField(db_collation='utf8mb4_unicode_ci', max_length=10000, null=True),
        ),
    ]