from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import *

user_router = DefaultRouter()
user_router.register(r'user-viewset/', UserViewSet, basename='users')

urlpatterns = [
    path('users/', include(user_router.urls)),
]
