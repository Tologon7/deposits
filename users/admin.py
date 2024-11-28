from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Подключение форм
    form = UserChangeForm
    add_form = UserCreationForm

    # Поля, отображаемые в списке пользователей
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    # Поля для редактирования пользователя
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name',
                'is_staff', 'is_active', 'is_superuser'
            ),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
