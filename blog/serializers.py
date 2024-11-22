from rest_framework import serializers
from blog.models import *


class BlogImageSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = [
            'id',
            'blog',
            'image'
        ]


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['image']


class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'name', 'category', 'description', 'coordinates1', 'coordinates2', 'images']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
        ]
