from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    phone_otp = models.CharField(max_length=6, null=True, blank=True )
    phone_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=25, null=True, blank=True )
    email_verified = models.BooleanField(default=False)
