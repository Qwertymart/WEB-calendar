from django.shortcuts import render

import datetime


def home(request):
    date = datetime.datetime.now().date()
    return render(request, 'home.html')
