from django.contrib import admin

from .models import *

admin.site.register(CustomToken)
admin.site.register(CustomTokenProxy)
