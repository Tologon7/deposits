from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт позволяет пользователям войти в систему, предоставив имя пользователя и пароль. "
                              "После успешного входа генерируются Access и Refresh токены."
    )
    def post(self, request, *args, **kwargs):
        # Используем сериализатор для обработки данных
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Если данные валидны, извлекаем токены
        tokens = serializer.validated_data
        return Response({
            'access': str(tokens['access']),
            'refresh': str(tokens['refresh']),
        }, status=status.HTTP_200_OK)



class UsersListView(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.all()
