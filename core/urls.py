from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-api/', include('User.urls')),
    path('rest-auth/', include('rest_auth.urls')),
]
