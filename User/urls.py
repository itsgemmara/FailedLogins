from django.urls import path, re_path
from .api import CreateUserApiView, LoginApi, UnblockCodeGeneratorApi, UnBlockApi, DeleteToken
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='User API')

urlpatterns = [

    path('register/', CreateUserApiView.as_view()),
    path('login/', LoginApi.as_view()),
    path('unblock-verify-code/', UnblockCodeGeneratorApi.as_view()),
    path('unblock-account/', UnBlockApi.as_view()),
    path('swagger/', schema_view),
    path('delete-token/', DeleteToken.as_view())

]
