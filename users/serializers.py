import random
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, OTP


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9!@#$%^&*()_+.-]+$',
                message='Username can only contain English letters, numbers, and special characters (!@#$%^&*()_+.-)',
            ),
        ],
        min_length=6,
        max_length=20,
        required=False
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')

        otp_code = str(random.randint(100000, 999999))
        validated_data['is_active'] = False
        validated_data['otp_code'] = otp_code
        validated_data['otp_created_at'] = timezone.now()

        send_mail(
            'Новый пользователь!',
            f"Имя: {validated_data['first_name']} {validated_data['last_name']} хочет зарегистрироваться.\n"
            f"Email: {validated_data['email']}\nКод для подтверждения: {otp_code}",
            'email',
            ['kubandykovtologon@gmail.com'],
            fail_silently=False,
        )

        user = User.objects.create(
            password=make_password(password),
            **validated_data
        )

        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')

        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or this account is not pending activation.')

        if user.otp_created_at is None:
            raise serializers.ValidationError('OTP code was not created or is invalid.')

        otp_lifetime = timedelta(days=3)  # Время жизни OTP: 3 дня
        if timezone.now() > user.otp_created_at + otp_lifetime:
            raise serializers.ValidationError('OTP code has expired.')

        if not user.otp_code or user.otp_code != otp_code:
            raise serializers.ValidationError('Invalid OTP code.')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        user.is_active = True
        user.otp_code = None
        user.otp_created_at = None
        user.save()
        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = self.user
        return data


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        try:
            token = RefreshToken(attrs['refresh'])
            token.blacklist()  # Поместите токен в черный список
        except Exception as e:
            raise serializers.ValidationError({'refresh': str(e)})
        return attrs


# forgot password
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        code = data.get('code')

        try:
            otp_obj = OTP.objects.get(otp=code)
            if otp_obj.is_expired:
                raise serializers.ValidationError({'error': "OTP has expired."})
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'error': "Invalid OTP."})

        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
        ]
