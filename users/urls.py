from django.urls import path

from .views import *

urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('list/', UsersListView.as_view(), name='user-list'),
    path('me/', UserMeView.as_view(), name='user-me'),


    # path('logout/', UserLogoutView.as_view(), name='logout'),
]