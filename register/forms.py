# Ваш файл forms.py

from django import forms
from .models import users

class UserForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['name', 'password']
