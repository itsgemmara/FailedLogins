from django.contrib import admin

from .models import CustomUser, Block, WrongPass, IP

admin.site.register(CustomUser)
admin.site.register(Block)
admin.site.register(WrongPass)
admin.site.register(IP)
