from django.shortcuts import render, get_object_or_404, redirect
from events.models import Event
from events.forms import EventForm

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if 'save' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('events')
        elif 'delete' in request.POST:
            event.delete()
            return redirect('events')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_editor/edit_event.html', {'form': form, 'event': event})
