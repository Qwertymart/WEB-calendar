from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль")

