from django.urls import path

from .views import *

urlpatterns = [

    path('login/', UserLoginView.as_view(), name='login'),
    path('list/', UsersListView.as_view(), name='user-list'),

    # path('logout/', UserLogoutView.as_view(), name='logout'),
]