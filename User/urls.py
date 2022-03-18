from django.urls import path

from .api import CreateUserApiView, LoginAPIView
from .validators import login_validator


urlpatterns = [
    path('register/', CreateUserApiView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('login/<str:phone_number>/<str:password>/', login_validator)

]
