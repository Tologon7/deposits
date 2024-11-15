from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from depo import settings
from users.models import OTP
from .serializers import *


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет возможность пользователям "
                              "зарегистрироваться в системе, предоставив необходимые данные. "
                              "После успешной регистрации создается новая запись пользователя и "
                              "отправляется 6-значный OTP-код на email администратора. "
                              "Пользователь должен ввести этот код в эндпоинте /users/wholesaler-otp/ "
                              "вместе с email, чтобы завершить регистрацию.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.otp_code:
                return Response(
                    {
                        'message': 'OTP-код отправлен на email администратора. '
                                   'Пожалуйста, введите этот код вместе с email, чтобы активировать учетную запись.'
                     },
                    status=status.HTTP_200_OK
                )
            else:
                user_data = UserRegistrationSerializer(user).data
                return Response({'user': user_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт позволяет пользователям завершить регистрацию, "
                              "предоставив полученный OTP-код.",
        request_body=OTPVerificationSerializer,
        responses={200: 'Регистрация прошла успешно!', 400: 'Неправильный OTP код или email :('}
    )
    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserRegistrationSerializer(user).data
            return Response({'user': user_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

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
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = data['user']
            tokens = {
                'access': str(data['access']),
                'refresh': str(data['refresh']),
            }
            user_data = UserRegistrationSerializer(user).data
            user_data['tokens'] = tokens
            return Response({'user': user_data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет пользователям"
                              " возможность выйти с аккаунта ",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_logout(serializer.validated_data['refresh'])
        return Response(status=status.HTTP_205_RESET_CONTENT)

    def perform_logout(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Вы успешно вышли с аккаунта."}, status=status.HTTP_200_OK)
        except Exception as e:
            raise serializers.ValidationError({'refresh': str(e)})


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предназначен "
                              "для пользователей, которые "
                              "забыли свой пароль. Пользователь "
                              "может запросить восстановление пароля, "
                              "предоставив свой номер телефона. Система якобы "
                              "отправит SMS с 4-значным кодом для восстановления "
                              "пароля, но на самом деле код будет храниться на "
                              "сервере для последующей проверки. После успешной "
                              "отправки номера телефона "
                              "система возвращает айди пользователя. \nКод подтверждения: 1991.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Пользователь с таким email не существует :("}, status=status.HTTP_404_NOT_FOUND)
            otp_code = OTP.generate_otp()
            OTP.objects.create(user=user, otp=otp_code)
            # Send the OTP to the user's email
            subject = 'Забыли пароль OTP'
            message = f'Ваш OTP код: {otp_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            return Response({"message": "OTP Код отправлен на вашу почту!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmCodeView(generics.GenericAPIView):
    serializer_class = ConfirmationCodeSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт позволяет "
                              "подтвердить код подтверждения, "
                              "который был отправлен на адрес "
                              "электронной почты пользователя "
                              "после успешной регистрации. После "
                              "подтверждения кода, система выдает новый "
                              "токен доступа (Access Token) и обновления "
                              "(Refresh Token) для пользователя.",
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')
        try:
            confirmation_code = OTP.objects.get(otp=code)
        except OTP.DoesNotExist:
            return Response({"error": "Неправильный код :("}, status=400)

        user = confirmation_code.user
        confirmation_code.delete()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Код успешно применен!",
            'user_id': str(user.id),
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    # permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=['User'],
        operation_description="Этот эндпоинт предоставляет администраторам"
                              " возможность получить список всех"
                              " аутентифицированных пользователей.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.all().order_by('-id').filter(is_active=True)
