from rest_framework.response import Response
from rest_framework import generics, mixins, views
from rest_framework.decorators import action
from rest_framework import viewsets

from .serializer import *
from .models import UnBlockCode
from .utils import UnblockCodeGeneratorApi, UnBlockApi
from Token.models import CustomToken


class UserViewSet(viewsets.ModelViewSet):
    """
    General ViewSet description

    list: List user

    retrieve: Retrieve user

    update: Update user

    create: Create user

    partial_update: Patch user

    login_user: login user

    destroy: Delete user
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UpdateUserSerializer
        elif self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserRetrieveSerializer
        elif self.action == 'login_user':
            return LoginSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [permissions.IsAuthenticated(), ]
            return permission_classes
        elif self.action == 'list':
            return [permissions.IsAdminUser(), ]
        return [permissions.AllowAny(), ]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(phone_number=self.request.user.phone_number)

    @action(detail=False, methods=['post', ])
    def login_user(self, a):
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(self.request, user)
        token = CustomToken.objects.create(user=user)
        return Response({"Token": token.key}, status=200)


class AccountViewSet(viewsets.GenericViewSet,):
    """
    General Account ViewSet description

    unblock_code_generator: unblock code generator

    unblock_account: unblock account
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', ]

    def get_serializer_class(self):
        if self.action == 'unblock_code_generator':
            return UnBlockCodeSerializer
        if self.action == 'unblock_account':
            return UnBlockSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(phone_number=self.request.user.phone_number)

    @action(detail=False, methods=['post', ])
    def unblock_code_generator(self, a):
        code = UnblockCodeGeneratorApi().post(self.request)
        # user = self.request.user
        # verify_code = UnBlockCode.objects.get(user=user, used=False, is_expired=False).code
        return Response(code, status=200)

    @action(detail=False, methods=['post', ])
    def unblock_account(self, a):
        unblock = UnBlockApi().post(self.request)
        return Response(unblock, status=200)
