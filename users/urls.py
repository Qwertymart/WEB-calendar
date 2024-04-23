from django.contrib import admin
from django.urls import path
from . import views
from register.views import register
from login.views import login_views
from events.views import events
app_name = 'users'

urlpatterns = [
    path('login1/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
]
