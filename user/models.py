from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.CharField(max_length=254, unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    phone_otp = models.CharField(max_length=6, null=True, blank=True )
    phone_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=25, null=True, blank=True )
    email_verified = models.BooleanField(default=False)
    verified_account = models.BooleanField(default=False)
    profile_imgg = models.FileField(upload_to="profile", null=True, blank=True)
    bg_imgg = models.FileField(upload_to="profile", null=True, blank=True)
    followers = models.ManyToManyField('user.User')
    bookmarks = models.ManyToManyField('Tweet', related_name='my_bookmarks')
    header_photo = models.FileField(upload_to="profile", null=True, blank=True)
    photo = models.FileField(upload_to="profile", null=True, blank=True)
    

class T_Media(models.Model):
    file_name = models.FileField(upload_to="tweets")


class Tags(models.Model):
    name = models.TextField( max_length=255, db_collation='utf8mb4_unicode_ci', unique=True)
    used_times = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    msg = models.TextField(db_collation='utf8mb4_unicode_ci', max_length=10000, null=True)

    TWEET_TYPES = (
        (0, 'Message'),
        (1, 'Media'),
        (2, 'Poll')
    )
    tweet_type = models.IntegerField(default=0, choices=TWEET_TYPES)

    REPLY_TYPES = (
        (0,'Everyone'),
        (1,'Accounts you follow'),
        (2,'Verified'),
        (3,'Only accounts mention')
    )

    reply_by = models.IntegerField(default=0, choices=REPLY_TYPES)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    mentions = models.ManyToManyField('user.User', related_name='mentioned_in_tweets')
    tweet_media =models.ManyToManyField(T_Media)
    tweet_tags =models.ManyToManyField(Tags)
    active_status = models.BooleanField(default=True)
    schedule_tym = models.DateTimeField(null=True, blank=True)
    end_tym = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    repost_tweet = models.ForeignKey('self', on_delete=models.CASCADE,related_name='repost_tweets', null=True, blank=True)
    total_reposts = models.IntegerField(default=0)
    likes = models.ManyToManyField('user.User', related_name='liked_by')
    total_likes = models.IntegerField(default=0)
    views = models.ManyToManyField('user.User', related_name='viewed_by')
    total_views = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)



