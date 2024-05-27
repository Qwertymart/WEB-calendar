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
from home.views import home
from events.views import events, week, day, new_event, generate_description, move_event
from event_editor.views import edit_event

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('users/', include('users.urls', namespace='users')),

    # Маршрут для отображения календаря по умолчанию

    path('events/', events, {'view_type': 'month'}, name='events'),
    path('events/week/', week, name='week'),
    path('events/day/', day, name='day'),
    path('events/new_event/', new_event, name='new_event'),
    path('events/generate_description/', generate_description, name='generate_description'),
    path('events/day/<int:selected_year>/<int:selected_month>/<int:selected_day>/', day, name='day_selected_day'),

    # Дополнительные маршруты для обработки различных действий или типов отображения

    path('events/week/<int:selected_year>/<int:selected_month>/<int:select_week>/', week, name='week_calendar_selected_week'),
    path('event/<int:event_id>/edit/', edit_event, name='edit_event'),
    path('move_event/', move_event, name='move_event'),

]
