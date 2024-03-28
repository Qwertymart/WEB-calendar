
from django.shortcuts import render, redirect
from .forms import UserForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'register/log.html')
