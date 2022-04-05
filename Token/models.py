from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token

from User.models import CustomUser


class CustomToken(Token):

    key = models.CharField("Key", max_length=40, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="User"
    )


class CustomTokenProxy(CustomToken):
    """
    Proxy mapping pk to user pk for use in admin.
    """
    @property
    def pk(self):
        return self.pk

    class Meta:
        proxy = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "token proxy"


