from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model # If used custom user model
from rest_framework.response import Response

from .serializers import UserSerializer, LoginSerializer


class CreateUserApiView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


class LoginAPIView(APIView):

    def post(self, request):
        data = {'phone_number': request}
        serializer = LoginSerializer(data=str(request.data))
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            message = f"login with : {phone_number}"
            return Response({'message': message, status: 'HTTP_200_OK'})
        else:
            return Response(
                serializer.error_messages,
                status=status.HTTP_400_BAD_REQUEST
            )

        #
        #
        # def get(self, request):
        #     wallet = CustomWallet()
        #     key = wallet.final_key
        #     address = wallet.final_address
        #     data = {'key': key, 'address': address}
        #     serializer = BTCWalletSerializer(data)
        #     return Response(serializer.data)


