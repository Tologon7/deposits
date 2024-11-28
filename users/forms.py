from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserCreationForm(forms.ModelForm):
    """
    Форма для создания нового пользователя с поддержкой всех полей.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Хэширование пароля
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Форма для обновления существующего пользователя с поддержкой всех полей.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password',
            'first_name', 'last_name',
            'is_staff', 'is_active', 'is_superuser'
        )

    def clean_password(self):
        # Возвращает пароль без изменений
        return self.initial["password"]
