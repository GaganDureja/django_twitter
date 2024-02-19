from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    phone_otp = models.CharField(max_length=6, null=True, blank=True )
    phone_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=25, null=True, blank=True )
    email_verified = models.BooleanField(default=False)
    verified_account = models.BooleanField(default=False)
    profile_imgg = models.FileField(upload_to="profile", null=True, blank=True)
    bg_imgg = models.FileField(upload_to="profile", null=True, blank=True)


class T_Media(models.Model):
    file_name = models.FileField(upload_to="tweets")


class Tags(models.Model):
    name = models.CharField(max_length=255, unique=True)
    used_times = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    msg = models.CharField(max_length=500, null=True)

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
    repost_tweet = models.IntegerField(default=0)
    mentions = models.ManyToManyField(User, related_name='mentioned_in_tweets', null=True, blank=True)
    tweet_media =models.ManyToManyField(T_Media, null=True, blank=True)
    tweet_tags =models.ManyToManyField(Tags, null=True, blank=True)
    active_status = models.BooleanField(default=True)
    schedule_tym = models.DateTimeField(null=True, blank=True)
    end_tym = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    total_likes = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)

# class Reply(models.Model):



class Likes(models.Model):
    # LIKE_TYPES = (
    #     (0, 'Tweet'),
    #     (1, 'Reply')        
    # )
    post_id = models.IntegerField()
    # type = models.IntegerField(default=0, choices=LIKE_TYPES)
    liked_by = models.ForeignKey(User,on_delete=models.CASCADE)


class Views(models.Model):
    # VIEW_TYPES = (
    #     (0, 'Tweet'),
    #     (1, 'Reply')        
    # )
    post_id = models.IntegerField()
    # type = models.IntegerField(default=0, choices=VIEW_TYPES)
    viewed_by = models.ForeignKey(User,on_delete=models.CASCADE)



# class ReplyTweet(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     reply_to = models.ForeignKey(Tweet, on_delete=models.CASCADE)
#     TWEET_TYPES = (
#         (0, 'Message'),
#         (1, 'Media'),
#     )
#     tweet_type = models.IntegerField(default=0, choices=TWEET_TYPES)
#     active_status = models.BooleanField(default=True)

#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)



class Following(models.Model):
    main_user = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following_to = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)


