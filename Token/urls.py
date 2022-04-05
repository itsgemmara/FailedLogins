from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import TokenViewSet

router = DefaultRouter()
router.register(r'user-tokens/', TokenViewSet, basename='tokens')

urlpatterns = [
    path('tokens/', include(router.urls)),
]
