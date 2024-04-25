from django.urls import path
from . import views

urlpatterns = [
    path('week/', views.week, name='week'),
    path('day', views.day, name='day'),
]
