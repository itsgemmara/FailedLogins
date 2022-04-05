from rest_framework.response import Response
from rest_framework import generics, mixins, views
from rest_framework.decorators import action
from rest_framework import viewsets
from django.core.exceptions import ValidationError

from .serializer import *
from .models import UnBlockCode
from .utils import UnblockCodeGeneratorApi, UnBlockApi
from Token.models import CustomToken


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet,
                  ):
    """
    General ViewSet description

    list: List user

    retrieve: Retrieve user

    update: Update user

    create: Create user

    partial_update: Patch user

    login_user: login user

    unblock_code_generator: unblock code generator

    unblock_account: unblock account

    deactivate_account: deactivate account

    show_pk: show pk for user by phone_number
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
        elif self.action == 'unblock_code_generator':
            return UnBlockCodeSerializer
        elif self.action == 'unblock_account':
            return UnBlockSerializer
        elif self.action == 'deactivate_account':
            return DeactivateSerializer
        elif self.action == 'show_pk':
            return ShowPkSerializer

        return UserSerializer

    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [permissions.IsAuthenticated(), ]
            return permission_classes
        elif self.action == 'list' and self.action == 'show_pk':
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

    @action(detail=False, methods=['post', ])
    def show_pk(self, a):
        serializer = ShowPkSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        user = get_object_or_404(CustomUser, phone_number=phone_number)
        return Response({'pk': user.pk}, status=200)

    @action(detail=False, methods=['post', ])
    def deactivate_account(self, a):
        serializer = DeactivateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        pk = serializer.validated_data["pk"]
        user = get_object_or_404(CustomUser, phone_number=phone_number, pk=pk)
        if not self.request.user.is_staff and not self.request.user.is_superuser and user != self.request.user:
            print(user, self.request.user,'444444444444444')
            raise ValidationError("you don't have any access to this account. please login first.")
        user.is_active = False
        user.save()
        return Response({'active': user.is_active}, status=200)

