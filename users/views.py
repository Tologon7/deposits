from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *


class UserLoginView(TokenObtainPairView):
    """Эндпоинт для входа пользователя с использованием токенов JWT."""

    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт позволяет пользователям войти в систему, предоставив имя пользователя и пароль. "
                              "После успешного входа генерируются Access и Refresh токены."
    )
    def post(self, request, *args, **kwargs):
        # Используем сериализатор для получения данных
        serializer = self.get_serializer(data=request.data)

        # Проверяем, валидны ли данные
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            tokens = {
                'access': str(validated_data['access']),
                'refresh': str(validated_data['refresh']),
            }
            return Response({'tokens': tokens}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)