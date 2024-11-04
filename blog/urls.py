from django.urls import path
from blog.views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog-list'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/', BlogIdView.as_view(), name='blog-detail-update')

]