from django.urls import path
from blog.views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    #blog
    path('list/', BlogListView.as_view(), name='blog-list'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/', BlogIdView.as_view(), name='blog-detail-update'),

    #image
    path('image/create/', BlogImageUploadView.as_view(), name='image-create'),

    #category
    path('category/create/', CategoryCreateView.as_view(), name='category-create')



]