from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import *


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get('refresh')
        try:
            RefreshToken(refresh)
        except Exception as e:
            raise serializers.ValidationError({'refresh': 'Invalid token.'})
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_superuser',
            'is_active'
        ]
