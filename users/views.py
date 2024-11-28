from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

from .serializers import *


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователям войти "
                              "в систему, предоставив имя пользователя "
                              "и пароль. После успешного входа, система "
                              "генерирует Access Token и Refresh Token для "
                              "пользователя, которые можно использовать для "
                              "доступа к защищенным ресурсам. \nСрок действия 'access' токена - "
                              "60 минут, а refresh токена - 30 дней.",
    )
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({"error": "User not found!"}, status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            raise AuthenticationFailed({"error": "Incorrect password!"})

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )

# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#
#     @swagger_auto_schema(
#         tags=['Authentication'],
#         operation_description=(
#             "Этот эндпоинт предоставляет возможность пользователям войти "
#             "в систему, предоставив имя пользователя и пароль. После успешного входа, "
#             "система генерирует Access Token и Refresh Token для пользователя, которые "
#             "можно использовать для доступа к защищенным ресурсам. \nСрок действия 'access' токена - "
#             "60 минут, а refresh токена - 30 дней."
#         ),
#     )
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#
#         if not username or not password:
#             return Response(
#                 {"error": "Username and password are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         # Аутентификация через встроенный метод
#         user = authenticate(username=username, password=password)
#
#         if user is None:
#             raise AuthenticationFailed({"error": "Invalid username or password."})
#
#         # Генерация токенов для пользователя
#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             },
#             status=status.HTTP_200_OK,
#         )

class UsersListView(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.all()


class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот ендпоинт предоставляет "
                              "возможность получить информацию "
                              "о текущем аутентифицированном пользователе. ",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)