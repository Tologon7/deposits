from django.urls import path
from blog.views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog-list')

]