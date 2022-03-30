from django.contrib import admin

from .models import CustomUser, Block, WrongPass, IP, UnBlockCode, CustomToken, CustomTokenProxy

admin.site.register(CustomUser)
admin.site.register(Block)
admin.site.register(WrongPass)
admin.site.register(IP)
admin.site.register(UnBlockCode)
admin.site.register(CustomToken)
admin.site.register(CustomTokenProxy)
