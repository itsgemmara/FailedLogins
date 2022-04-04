from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins

from .serializer import *


class TokenViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet,
                   mixins.DestroyModelMixin,
                   ):
    """
    A ViewSet for listing, retrieving, deleting and some another actions for tokens.

    list: List tokens

    destroy: destroys a single token object selected by `id`

    delete_token: deleting a token by another one.
    """
    queryset = CustomToken.objects.all()
    serializer_class = TokensListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TokensListSerializer
        elif self.action == 'destroy':
            return DestroyTokenSerializer
        elif self.action == 'delete_token':
            return DeleteTokenSerializer
        return TokensListSerializer

    def get_permissions(self):
        if self.action == 'delete_token' and self.action == 'list':
            permission_classes = [permissions.IsAuthenticated(), ]
            return permission_classes
        elif self.action == 'destroy':
            return [permissions.IsAdminUser(), ]
        return [permissions.AllowAny(), ]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(phone_number=self.request.user.phone_number)

    @action(detail=False, methods=['post'])
    def delete_token(self, request):
        """
        The delete_token action deletes a token by another one.
        """
        serializer = DeleteTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        target_token = serializer.validated_data["target_token"]
        target_token.delete()
        return Response(status=200)
