from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from User.models import CustomUser
from .validators import login_username_validator, ip_validator


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
        fields = ("phone_number", "password", "password2")


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ("phone_number", "first_name", "last_name", "email")


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ("phone_number", "pk")


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ("phone_number", "first_name", "last_name", "email", "date_joined")


class LoginSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, validated_data):
        username_access_to_login = login_username_validator(self.context['request'],
                                          validated_data['phone_number'], validated_data['password'])
        ip_access_to_login = ip_validator(self.context['request'])
        if validated_data['phone_number'] and validated_data['password']:
            user = authenticate(phone_number=validated_data['phone_number'], password=validated_data['password'])
            if user:
                if user.is_active:
                    if not user.is_locked:
                        validated_data["user"] = user
                    else:
                        raise ValidationError("User account is Locked.")
                else:
                    raise ValidationError("User is deactivated.")
                return validated_data
            raise ValidationError("unable to login")
        raise ValidationError("Must provide phone number and password both.")

    class Meta:
        model = UserModel
        fields = ("phone_number", "password",)


class UnBlockSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verify_code = serializers.CharField()

    def validate(self, validated_data):

        if validated_data['phone_number'] and validated_data['verify_code']:
            user = get_object_or_404(CustomUser, phone_number=validated_data['phone_number'])
            if user:
                validated_data["user"] = user
                return validated_data
            raise ValidationError("no user with this phone number")


class UnBlockCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_code = serializers.BooleanField()

    def validate(self, validated_data):

        if validated_data['phone_number']:
            user = get_object_or_404(CustomUser, phone_number=validated_data['phone_number'])
            if user:
                if user.is_active and not user.is_locked:
                    raise ValidationError("your account alredy is active and unblock.")
                validated_data["user"] = user
                return validated_data
            raise ValidationError("no user with this phone number")

