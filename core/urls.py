from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='User API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('User.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('tokens/', include('Token.urls')),
    path('swagger/', schema_view),
]
