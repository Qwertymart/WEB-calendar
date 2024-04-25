"""
URL configuration for TimeTracer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home
from register.views import register
from login.views import login_views
from events.views import events, week, day

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('', register),
    path('users/', include('users.urls', namespace='users')),
    path('login/', login_views, name='login'),
    path('events/', events, name='events'),
    path('events/week/', week, name='week'),
    path('events/day/', day, name='day'),
]