from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    def validate(self, validated_data):

        if validated_data['password'] == validated_data['password2']:
            return validated_data
        raise ValidationError("Enter same password!")

    def create(self, validated_data):

        password = validated_data['password']
        password2 = validated_data['password2']
        phone_number = validated_data['phone_number']

        if self.validate(validated_data):
            user = UserModel.objects.create_user(
                phone_number,
                password
            )
            return user
        else:
            raise ValidationError("Enter same password!")

    class Meta:
        model = UserModel
        fields = ("phone_number", "password", "password2",)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


