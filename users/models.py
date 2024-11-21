# models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователи должны иметь адрес электронной почты')
        if not username:
            raise ValueError('Пользователи должны иметь имя пользователя')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        # Сохраняем пароль как обычный текст (без хеширования)
        user.password = password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# class OTP(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=4, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     @staticmethod
#     def generate_otp():
#         digits = string.digits
#         return ''.join(random.choice(digits) for i in range(4))
#
#     @property
#     def is_expired(self):
#         time_threshold = timezone.now() - timezone.timedelta(minutes=5)
#         return self.created_at < time_threshold
