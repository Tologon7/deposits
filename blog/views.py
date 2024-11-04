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


class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all
    serializer_class = BlogSerializer

    @swagger_auto_schema(
        tags=['blog'],
        operation_description="Этот эндпоинт позволяет создать новое месторождение."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BlogIdView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить месторождение по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет обновить(присвоить другие данные) месторождение по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет удалить месторождение по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
