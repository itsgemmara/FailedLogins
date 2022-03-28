from django.urls import path

from .api import CreateUserApiView, LoginApi, UnblockCodeGeneratorApi, UnBlockApi


urlpatterns = [
    path('register/', CreateUserApiView.as_view()),
    path('login/', LoginApi.as_view()),
    path('unblock-verify-code/', UnblockCodeGeneratorApi.as_view()),
    path('unblock-account/', UnBlockApi.as_view())


]
