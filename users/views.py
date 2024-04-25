from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login1.html'
    extra_context = {'title': 'Авторизация'}


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('users:login')
    else:
        form = RegisterUserForm()

    return render(request, 'users/register.html', {'form': form})
