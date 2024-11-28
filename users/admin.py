from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_superuser')
    list_filter = ('is_active', 'is_superuser')
    search_fields = ('username', 'email')
