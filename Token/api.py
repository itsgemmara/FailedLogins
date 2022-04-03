from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView

from .models import CustomToken
from .serializer import *


class TokenViewSet(viewsets.ViewSet, permissions.IsAuthenticated):
    """
    A ViewSet for listing, retrieving, deleting and some another actions for tokens.
    """
    queryset = CustomToken.objects.all()

    def list(self, request):
        """
        The list action returns all available tokens.
        """
        queryset = self.queryset.filter(user=request.user)
        serializer = TokensListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        The retrieve action returns a single object selected by 'id'.
        """
        queryset = self.queryset.filter(user=request.user)
        token = get_object_or_404(queryset, pk=pk)
        serializer = DestroyTokenSerializer(token)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        The destroy action destroys a single object selected by `id`
        """
        queryset = self.queryset.filter(user=request.user)
        token = get_object_or_404(queryset, pk=pk)
        serializer = DestroyTokenSerializer(data={'key': token.key, 'pk': pk, 'created': token.created})
        serializer.is_valid(raise_exception=True)
        token.delete()
        return Response('done', status=200)

    @action(detail=False, methods=['post'])
    def delete_token(self, request, serializer_class, pk=None):
        """
        The delete_token action deletes a token by another one.
        """
        serializer = DeleteTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        target_token = serializer.validated_data["target_token"]
        target_token.delete()
        return Response(status=200)


class DeleteToken(GenericAPIView, permissions.IsAuthenticated):
    """
    deleting a token by another one.
    """
    serializer_class = DeleteTokenSerializer

    def post(self, request):
        serializer = DeleteTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        target_token = serializer.validated_data["target_token"]
        target_token.delete()
        return Response(status=200)

