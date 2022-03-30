from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import binascii
import os
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


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

    ip = models.CharField(max_length=15,unique=True)
    date_created = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(default=False)


class WrongPass(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    state = models.IntegerField(default=0, null=True)
    ip = models.ForeignKey(IP, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.phone_number}:{self.state}"


class Block(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)  # interval start date
    count_of_wrong_pass = models.IntegerField(default=1, null=True)

    def __str__(self):
        return f"{self.user.phone_number}:{self.count_of_wrong_pass}"


class UnBlockCode(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    used = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True)


class CustomToken(Token):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )


class CustomTokenProxy(CustomToken):
    """
    Proxy mapping pk to user pk for use in admin.
    """
    @property
    def pk(self):
        return self.user_id

    class Meta:
        proxy = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "token proxy"
