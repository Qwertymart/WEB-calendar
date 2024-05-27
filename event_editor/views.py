from django.shortcuts import render, get_object_or_404, redirect
from events.models import Event
from events.forms import EventForm


def edit_event(request, event_id):
    """
        Редактирует событие. Позволяет изменить все параметры события.

        Parameters
        ----------
        request : HttpRequest
            Запрос от клиента.
        event_id : int
            Идентификатор события.

        Returns
        -------
        HttpResponse
            Ответ с отрендеренной страницей редактирования события.
        """
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
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
