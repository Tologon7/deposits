from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register-otp/', OTPVerificationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('confirm-code/', ConfirmCodeView.as_view(), name='confirm-code'),
    path('user-list/', UserListView.as_view(), name='user-list'),
]