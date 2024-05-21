from django.urls import path
from . import views

urlpatterns = [
    path('week/', views.week, name='week'),
    path('day/', views.day, name='day'),
    path('', views.events, {'view_type': view_type}, name='events'),
    path('new_event/', views.new_event, name='new_event'),
    path('generate_description/', views.generate_description, name='generate_description'),
]
