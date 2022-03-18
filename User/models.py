from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):

    username = None
    phone_number = models.CharField('phone number', max_length=11,  unique=True)
    number_of_user_blocking = models.IntegerField(default=0, null=True)
    number_of_IP_blocking = models.IntegerField(default=0, null=True)
    is_locked = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class IP(models.Model):

    username = models.CharField(max_length=255)
    ip = models.CharField(max_length=15)
    count_faild_login = models.IntegerField(default=0, null=True)


class WrongPass(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    user_IP = models.OneToOneField(IP, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    state = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.user.phone_number}:{self.state}"


class Block(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=True)
    date = models.DateTimeField(auto_now=True)  # interval start date
    count_of_wrong_pass = models.IntegerField(default=1, null=True)

    def __str__(self):
        return f"{self.user.phone_number}:{self.count_of_wrong_pass}"


