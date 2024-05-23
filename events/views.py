# views.py
from django.shortcuts import render, redirect
from .forms import EventForm, ViewTypeForm, YEARS, DateSelectionForm
from .models import Event as Event
from .models import Notification
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from calendar import monthrange
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
auth = 'OWRjNWE4YjgtYmNiZC00YTNlLThmM2EtMzM3ODQxZmM0ODY0Ojk5M2RmY2E4LWI4ZDEtNGI4Yi05ZmQ1LWU3NzBkMGNhYWQ3OQ=='
chat = GigaChat(credentials=auth, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Помогите пользователю написать краткое описание события на основе его названия."
    )
]


def week_view(request, select_week, selected_month, selected_year):
    form = EventForm()
    if request.method == 'GET':
        # Проверка на передачу года, месяца и недели
        selected_month = int(request.GET.get('selected_month', selected_month))
        selected_year = int(request.GET.get('selected_year', selected_year))
        selected_week = int(request.GET.get('select_week', select_week))
    else:
        selected_month = int(selected_month)
        selected_year = int(selected_year)
        selected_week = int(select_week)

    for value in YEARS:
        if value[1] == str(selected_year):
            name = value

    first_weekday, num_days = monthrange(selected_year, selected_month)
    num_padding_days = (first_weekday) % 7
    days_of_month = []
    week_of_month = []
    for i in range(num_padding_days):
        week_of_month.append(None)
    for day_of_month in range(1, num_days + 1):
        week_of_month.append(datetime(selected_year, selected_month, day_of_month))
        if len(week_of_month) == 7:
            days_of_month.append(week_of_month)
            week_of_month = []
    if week_of_month:
        while len(week_of_month) < 7:
            week_of_month.append(None)
        days_of_month.append(week_of_month)

    current_week = days_of_month[int(selected_week) - 1] if 1 <= int(selected_week) <= len(days_of_month) else \
    days_of_month[0]
    week_counter = len(days_of_month)
    options = [{'value': f'{number + 1}', 'label': f'{number + 1}'} for number in range(week_counter)]

    hours_str = ['00:00'] + [f"{hour:02d}:00" for hour in range(1, 24)]
    hours = [datetime.strptime(hour, '%H:%M') for hour in hours_str]

    notification = Notification.objects.filter(user=request.user)
    events = Event.objects.filter(
        date_start__year=selected_year,
        date_start__month=selected_month,
        user=request.user
    )

    month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
             'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    current_year = timezone.now().year
    current_month = timezone.now().month

    context = {
        'selected_month': month[selected_month - 1], 'form': form, 'events': events,
        'selected_year': selected_year, 'hours': hours,
        'days_of_month': days_of_month, 'current_week': current_week,
        'options': options, 'select_week': selected_week, 'current_month': month[current_month - 1],
        'notification': notification, 'current_year': current_year, 'month': selected_month
    }

    return context


def events(request, view_type='month'):

    user_events = Event.objects.filter(user=request.user)

    for event in user_events:

        date_start_datetime = datetime.combine(event.date_start, event.time_start)
        now_with_timezone = timezone.localtime(timezone.now())
        date_start_aware = date_start_datetime.replace(tzinfo=timezone.utc)
        time_difference = date_start_aware - now_with_timezone

        if time_difference <= timedelta(hours=1) and time_difference.total_seconds() > 0:
            if not Notification.objects.filter(user=request.user, event=event).exists():
                notification_time = event.date_start - timedelta(hours=1)
                notification = Notification(user=request.user, text=f"Время начала события '{event.name}' через час",
                                            created_at=notification_time, event=event)
                notification.save()

    def month_view():
        form = EventForm()
        current_year = timezone.now().year
        current_month = timezone.now().month

        selected_month = int(request.GET.get('selected_month', current_month))
        selected_year = int(request.GET.get('selected_year', current_year))

        first_weekday, num_days = monthrange(selected_year, selected_month)

        num_padding_days = (first_weekday) % 7
        days_of_month = []
        week = []
        for i in range(num_padding_days):
            week.append(None)
        for day in range(1, num_days + 1):
            week.append(datetime(selected_year, selected_month, day))
            if len(week) == 7:
                days_of_month.append(week)
                week = []
        if week:
            while len(week) < 7:
                week.append(None)
            days_of_month.append(week)

        events = Event.objects.filter(date_start__year=selected_year, date_start__month=selected_month,
                                      user=request.user)
        notification = Notification.objects.filter(user=request.user)
        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
                 'Сентябрь', 'Август', 'Ноябрь', 'Декабрь']

        context = {'form': form, 'events': events, 'current_month': month[current_month - 1],
                   'current_year': current_year, 'selected_year': selected_year,
                   'days_of_month': days_of_month, 'selected_month': month[selected_month - 1],
                   'notification': notification, 'month': selected_month}
        return context

    description_event = ''
    if 'exit' in request.GET:
        return redirect('users:logout')

    elif 'new_event' in request.GET:
        return redirect('/events/new_event')

    if request.method == 'POST':
        if 'my_button' in request.POST:
            return redirect('home')
        elif 'delete_event_id' in request.POST:  # Проверяем, было ли отправлено сообщение об удалении
            event_id = request.POST.get('delete_event_id')
            event = Event.objects.get(id=event_id)
            event.delete()  # Удаляем событие
            return redirect('/events')  # Перенаправляем обратно на страницу событий после удалени
            # я
        elif 'new_event' in request.GET:
            return redirect('/new_event')

    else:  # else для method GET
        view_type = request.GET.get('view_type', view_type)
        if view_type == 'week':
            return redirect('week')
        elif view_type == 'day':
            return redirect('day')
        elif view_type == 'month':
            calendar_data = month_view()
            template_name = 'events/events.html'
        else:
            return render(request, 'events/error.html', {'message': 'Неизвестный тип отображения'})
        return render(request, template_name, calendar_data)
    form = EventForm()

    current_year = timezone.now().year
    current_month = timezone.now().month

    selected_month = int(request.GET.get('selected_month', current_month))
    selected_year = int(request.GET.get('selected_year', current_year))

    first_weekday, num_days = monthrange(selected_year, selected_month)

    num_padding_days = (first_weekday) % 7
    days_of_month = []
    week = []
    for i in range(num_padding_days):
        week.append(None)
    for day in range(1, num_days + 1):
        week.append(datetime(selected_year, selected_month, day))
        if len(week) == 7:
            days_of_month.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append(None)
        days_of_month.append(week)

    events = Event.objects.filter(date_start__year=selected_year, date_start__month=selected_month, user=request.user)
    notification = Notification.objects.filter(user=request.user)
    month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
             'Сентябрь', 'Август', 'Ноябрь', 'Декабрь']
    context = {'form': form, 'events': events, 'current_month': month[current_month - 1],
               'current_year': current_year, 'selected_month': month[selected_month - 1],
               'selected_year': selected_year,
               'days_of_month': days_of_month, 'notification': notification, 'month': selected_month}
    return render(request, 'events/events.html', context)


def week(request, selected_month=None, selected_year=None, select_week=None):
    if selected_year is None:
        selected_year = timezone.now().year
    if selected_month is None:
        selected_month = timezone.now().month
    if select_week is None:
        select_week = get_week_number_in_month(timezone.now())
    view_type = 'week'

    if 'exit' in request.GET:
        return redirect('users:logout')

    elif 'new_event' in request.GET:
        return redirect('/events/new_event')

    if request.method == 'POST':
        if 'my_button' in request.POST:
            return redirect('home')
        elif 'delete_event_id' in request.POST:
            event_id = request.POST.get('delete_event_id')
            event = Event.objects.get(id=event_id)
            event.delete()
            return redirect('week')
        else:
            event_name = request.POST.get('name', None)
            messages.append(HumanMessage(content=event_name))
            res = chat(messages)
            messages.append(res)
            description_event = res.content

            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.description = description_event
                event.save()
                return redirect('week')
    else:
        form_day = DateSelectionForm()
        view_type = request.GET.get('view_type', view_type)
        if view_type == 'day':
            return redirect('day')
        elif view_type == 'month':
            return redirect('events')

    select_week = request.GET.get('select_week', select_week)
    selected_month = request.GET.get('selected_month', selected_month)
    selected_year = request.GET.get('selected_year', selected_year)

    if select_week is None:
        select_week = get_week_number_in_month(timezone.now())
    if selected_month is None:
        selected_month = timezone.now().month
    if selected_year is None:
        selected_year = timezone.now().year

    calendar_data = week_view(request, select_week, selected_month, selected_year)
    template_name = 'events/week.html'

    if 'week_to_show' in request.GET:
        return redirect('week_calendar_selected_week', selected_year, selected_month, select_week)

    return render(request, template_name, calendar_data)

def day(request, selected_month=None, selected_year=None, selected_day=None):
    if selected_day is None:
        selected_day = timezone.now().day
    if selected_month is None:
        selected_month = timezone.now().month
    if selected_year is None:
        selected_year = timezone.now().year
    view_type = 'day'

    if 'exit' in request.GET:
        return redirect('users:logout')
    elif 'new_event' in request.GET:
        return redirect('/events/new_event')

    if request.method == 'POST':
        form_day = DateSelectionForm(request.POST)
        if form_day.is_valid():
            selected_date = form_day.cleaned_data['selected_date']
            selected_year = selected_date.year or selected_year
            selected_month = selected_date.month or selected_month
            selected_day = selected_date.day or selected_day

        if 'my_button' in request.POST:
            return redirect('home')
        elif 'delete_event_id' in request.POST:
            event_id = request.POST.get('delete_event_id')
            event = Event.objects.get(id=event_id)
            event.delete()  # Удаляем событие
            return redirect('day')  # Перенаправляем обратно на страницу событий после удаления
        elif 'select_day' in request.POST:
            return redirect('day_selected_day', selected_year, selected_month, selected_day)
        else:
            event_name = request.POST.get('name', None)
            messages.append(HumanMessage(content=event_name))
            res = chat(messages)
            messages.append(res)
            description_event = res.content

        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('day')
    else:
        form_day = DateSelectionForm()
        view_type = request.GET.get('view_type', view_type)
        if view_type == 'week':
            return redirect('week')
        elif view_type == 'month':
            return redirect('events')


    first_weekday, num_days = monthrange(selected_year, selected_month)
    num_padding_days = (first_weekday) % 7
    days_of_month = []
    week_of_month = []
    for _ in range(num_padding_days):
        week_of_month.append(None)
    for day_of_month in range(1, num_days + 1):
        week_of_month.append(datetime(selected_year, selected_month, day_of_month))
        if len(week_of_month) == 7:
            days_of_month.append(week_of_month)
            week_of_month = []
    if week_of_month:
        while len(week_of_month) < 7:
            week_of_month.append(None)
        days_of_month.append(week_of_month)

    events = Event.objects.filter(date_start__year=selected_year,
                                  date_start__month=selected_month,
                                  user=request.user)
    month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
                   'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    hours_str =['00:00'] + [f"{hour:02d}:00" for hour in range(1, 24)]
    hours = [datetime.strptime(hour, '%H:%M') for hour in hours_str]

    notification = Notification.objects.filter(user=request.user)
    form = EventForm()

    calendar_data = {
        'form': form, 'form_day': form_day, 'events': events,
        'selected_month': month[selected_month - 1],
        'month': selected_month,
        'selected_year': selected_year, 'days_of_month': days_of_month,
        'selected_day': selected_day,
        'hours': hours, 'notification': notification}

    return render(request, 'events/day.html', calendar_data)

@csrf_exempt
def generate_description(request):
    if request.method == "POST":
        event_name = request.POST.get('name', None)
        messages.append(HumanMessage(content=event_name))
        res = chat(messages)
        messages.append(res)
        description_event = res.content
        return JsonResponse({'description': description_event})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def new_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            periodicity = form.cleaned_data['periodicity']
            end_date = form.cleaned_data.get('end_date')
            date_start = form.cleaned_data['date_start']
            time_start = form.cleaned_data['time_start']
            date_finish = form.cleaned_data['date_finish']
            time_finish = form.cleaned_data['time_finish']

            event.save()

            if periodicity != 'no repeat' and end_date:
                current_date = date_start

                while True:
                    if periodicity == 'daily':
                        current_date += timedelta(days=1)
                    elif periodicity == 'weekly':
                        current_date += timedelta(weeks=1)
                    elif periodicity == 'monthly':
                        current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(
                            day=date_start.day)
                    elif periodicity == 'yearly':
                        current_date = current_date.replace(year=current_date.year + 1)

                    if current_date > end_date:
                        break

                    new_event = Event(
                        name=event.name,
                        date_start=current_date,
                        time_start=time_start,
                        date_finish=current_date,
                        time_finish=time_finish,
                        description=event.description,
                        color=event.color,
                        user=request.user  # Установите текущего пользователя
                    )
                    new_event.save()
            return redirect('/events')

    else:
        form = EventForm()
    return render(request, 'events/new_event.html', {'form': form})


def get_week_number_in_month(date):
    first_day_of_month = date.replace(day=1)
    day_of_month = date.day
    week_number = (day_of_month + first_day_of_month.weekday()) // 7 + 1
    return week_number

@csrf_protect
def move_event(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        new_date = request.POST.get("new_date")

        print("Event ID:", event_id)
        print("New Date:", new_date)

        try:
            event = Event.objects.get(id=event_id)
            event.date_start = datetime.strptime(new_date, "%Y-%m-%d").date()
            event.date_finish = event.date_start  # если событие однодневное
            event.save()
            print("Event updated:", event)  # Добавлено для отладки
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Событие не найдено'})
        except Exception as e:
            print("Error:", str(e))  # Добавлено для отладки
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
