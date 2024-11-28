# Register your models here.
from django.contrib import admin
from .models import Category, Blog, BlogImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'latitude', 'longitude')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'uploaded_at')
    list_filter = ('blog',)
