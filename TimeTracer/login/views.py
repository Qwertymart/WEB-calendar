import logging

from django.shortcuts import render, redirect
from register.forms import UserForm
from register.models import users

logger = logging.getLogger(__name__)

def login_views(request):
    error = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            password = request.POST.get('password')
            user = users.objects.filter(name=name).first()
            if user is not None and user.password == password:
                return redirect('home/')
            else:
                error = 'Неверное Имя или Пароль'
    else:
        form = UserForm()
    data = {
        'error': error,
        'form': form
    }
    return render(request, 'login/login.html', data)
