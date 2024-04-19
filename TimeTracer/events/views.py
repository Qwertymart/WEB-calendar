from django.shortcuts import render, redirect
from .forms import EventForm
from .models import events as Event
from django.utils import timezone

def events(request):
    if request.method == 'POST':
        if 'my_button' in request.POST:
            return redirect('home')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('events')
    else:
        form = EventForm()

    layout = request.GET.get('layout')
    month = request.GET.get('month')
    week = request.GET.get('week')

    current_year = timezone.now().year
    current_month = timezone.now().month

    if layout == 'week':
        events = Event.objects.filter()
    else:
        events = Event.objects.filter()

    return render(request, 'events/events.html', {'form': form, 'events': events, 'current_month': current_month, 'current_year': current_year})
