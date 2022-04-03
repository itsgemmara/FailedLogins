from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import CustomToken


class TokensListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomToken
        fields = ("pk", "key", "created")


class DestroyTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomToken
        fields = ("pk",)


class DeleteTokenSerializer(serializers.Serializer):
    user_token = serializers.CharField()
    token_to_delete = serializers.CharField()

    def validate(self, validated_data):
        if validated_data['user_token'] and validated_data['token_to_delete']:
            if validated_data['user_token'] != validated_data['token_to_delete']:
                main_token = get_object_or_404(CustomToken, key=validated_data['user_token'])
                target_token = get_object_or_404(CustomToken, key=validated_data['token_to_delete'])
                if (main_token.user == self.context['request'].user) and (main_token.user == target_token.user):
                    validated_data["target_token"] = target_token
                    return validated_data
                else:
                    raise ValidationError("invalid token")
            else:
                raise ValidationError("tokens are the same")
        else:
            raise ValidationError("tokens are required")
