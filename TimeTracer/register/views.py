from django.shortcuts import render, redirect
from .forms import UserForm
from .models import users
import hashlib


def register(request):
    error = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        name = request.POST.get('name')
        if form.is_valid():
            if not (users.objects.filter(name=name).exists()):
                if password == password_repeat:
                    password = hashlib.sha256(password.encode()).hexdigest()
                    user = users(name=name, password=password)
                    user.save()
                    return redirect('home')
                else:
                    error = 'Пароли отличаются друг от друга'
            else:
                error = 'Данное имя пользователя уже существует'
        else:
            error = 'Неверно введенная форма'

    form = UserForm(request.POST)

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'register/log.html', data)
