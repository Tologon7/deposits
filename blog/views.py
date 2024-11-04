from django.shortcuts import render

from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from blog.models import *
from blog.serializers import *


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    @swagger_auto_schema(
        tags=['blog'],
        operation_description="Этот эндпоинт позволяет получить список всех месторождений."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'request': self.request}

