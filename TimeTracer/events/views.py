# views.py
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import events as Event
from django.utils import timezone
from datetime import datetime
from calendar import monthrange

def events(request):
    if request.method == 'POST':
        if 'my_button' in request.POST:
            return redirect('home')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/events')
    else:
        form = EventForm()

    current_year = timezone.now().year
    current_month = timezone.now().month

    selected_month = int(request.GET.get('selected_month', current_month))

    # Calculate the number of days in the selected month
    _, num_days = monthrange(current_year, selected_month)

    # Get the first day of the selected month
    first_day = datetime(current_year, selected_month, 1)

    # Calculate the weekday of the first day (0 - Monday, 6 - Sunday)
    first_weekday = first_day.weekday()

    # Calculate the number of days to pad before the first day of the month in the calendar
    num_padding_days = (first_weekday) % 7

    # Generate a list of days for the selected month
    days_of_month = []
    week = []
    for i in range(num_padding_days):
        week.append(None)
    for day in range(1, num_days + 1):
        week.append(datetime(current_year, selected_month, day))
        if len(week) == 7:
            days_of_month.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append(None)
        days_of_month.append(week)

    # Retrieve events for the selected month
    events = Event.objects.filter(date_start__year=current_year, date_start__month=selected_month)

    return render(request, 'events/events.html',
                  {'events': events, 'current_month': current_month, 'current_year': current_year,
                   'days_of_month': days_of_month})
