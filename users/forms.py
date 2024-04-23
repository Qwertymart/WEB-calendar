from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    #username = forms.CharField(label="Логин")
    #password = forms.CharField(label="Пароль")

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')