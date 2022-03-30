import random
from django.utils import timezone
import threading
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import permissions

from .serializers import *
from .models import UnBlockCode, CustomToken
from .utils import activate_user_account


class CreateUserApiView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


class LoginApi(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        permission_classes = [
            permissions.AllowAny  # Or anon users can't register
        ]
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception= True)
        user = serializer.validated_data["user"]
        login(request, user)
        token = CustomToken.objects.create(user=user)
        return Response({"Token": token.key}, status=200)


class UnBlockApi(GenericAPIView):
    serializer_class = UnBlockSerializer

    def post(self, request):
        serializer = UnBlockSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception= True)
        user = serializer.validated_data["user"]
        verify_code = serializer.validated_data["verify_code"]
        try:
            main_code = UnBlockCode.objects.get(user=user, used=False, is_expired=False)
            activate_user_account(user, main_code, verify_code)
        except Exception as ex:
            raise Exception('invalid code. Enter the code correctly or request a new code.')

        return Response(status=200)


class UnblockCodeGeneratorApi(GenericAPIView):
    serializer_class = UnBlockCodeSerializer

    def __init__(self, code=None):
        self.code = code

    def set_is_expired(self):
        self.code.is_expired = True
        self.code.expired_at = timezone.now()
        self.code.save()
        return self.code

    def post(self, request):
        serializer = UnBlockCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        new_code_status = serializer.validated_data["new_code"]
        unexpired_codes = UnBlockCode.objects.filter(user=user, used=False, is_expired=False)
        if unexpired_codes.count() == 0 or new_code_status:
            verify_code = random.randint(10000, 99999)
            if unexpired_codes.count() != 0:
                for i in unexpired_codes:
                    i.is_expired = True
                    i.save()
            self.code = UnBlockCode.objects.create(code=verify_code, user=user)
            t = threading.Timer(interval=120, function=self.set_is_expired)
            t.start()
            return Response({"verify_code": verify_code}, status=200)
        elif unexpired_codes.count() == 1 and not new_code_status:
            verify_code = UnBlockCode.objects.get(user=user, used=False, is_expired=False).code
            return Response({"verify code": verify_code}, status=200)


class DeleteToken(GenericAPIView, permissions.IsAuthenticated):
    serializer_class = DeleteTokenSerializer

    def post(self, request):
        serializer = DeleteTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        target_token = serializer.validated_data["target_token"]
        target_token.delete()
        return Response(status=200)
