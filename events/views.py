# views.py
from django.shortcuts import render, redirect
from .forms import EventForm, ViewTypeForm, YEARS, DateSelectionForm
from .models import Event as Event
from .models import Notification
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from calendar import monthrange
from django.views.decorators.csrf import csrf_exempt

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

    # Корректное получение текущей недели
    current_week = days_of_month[int(selected_week) - 1] if 1 <= int(selected_week) <= len(days_of_month) else days_of_month[0]
    week_counter = len(days_of_month)
    options = [{'value': f'{number + 1}', 'label': f'{number + 1}'} for number in range(week_counter)]

    hours_str = [f"{hour:02d}:00" for hour in range(1, 24)]
    hours_str.append('00:00')
    hours = [datetime.strptime(i, '%H:%M') for i in hours_str]

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
        'selected_year': YEARS[YEARS.index(name)][1], 'hours': hours,
        'days_of_month': days_of_month, 'current_week': current_week,
        'options': options, 'select_week': selected_week, 'current_month': month[current_month - 1],
        'notification': notification, 'current_year': current_year
    }

    return context



def get_week_number_in_month(date):
    first_day_of_month = date.replace(day=1)
    day_of_month = date.day
    week_number = (day_of_month + first_day_of_month.weekday()) // 7 + 1
    return week_number

def events(request, view_type='month'):
    def select_view():
        # Если нажата кнопка submit при выборе отображения
        if 'view_button' in request.GET:
            temp = request.GET.get('view type', None)  # Получаем, что выбрали
            if temp == 'month':
                return redirect('events')  # Остаемся в той же вкладке
            elif temp == 'week':
                return redirect('week')  # Летим в week, чтобы уже работать в функции week на новой странице
            elif temp == 'day':
                return redirect('day')

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
        view_type = request.GET.get('view type', view_type)
        print(view_type)
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


def week(request, select_week=None, selected_month=None, selected_year=None):
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
        if 'view_button' in request.GET:
            form = ViewTypeForm()
            temp = request.GET.get('view type', None)
            if temp == 'month':
                return redirect('events')
            elif temp == 'week':
                return redirect('week')
            elif temp == 'day':
                return redirect('day')

    select_week = request.GET.get('select_week', select_week)
    selected_month = request.GET.get('selected_month', selected_month)
    selected_year = request.GET.get('selected_year', selected_year)

    if select_week is None:
        select_week = get_week_number_in_month(timezone.now()) - 1
    if selected_month is None:
        selected_month = timezone.now().month
    if selected_year is None:
        selected_year = timezone.now().year

    calendar_data = week_view(request, select_week, selected_month, selected_year)
    template_name = 'events/week.html'

    if 'week_to_show' in request.GET:
        return redirect('week_calendar_selected_week', selected_year, selected_month, select_week)

    return render(request, template_name, calendar_data)


def day(
        request,
        selected_month=timezone.now().month,
        selected_year=timezone.now().year,
        selected_day=timezone.now().day
):
    if 'exit' in request.GET:
        return redirect('users:logout')

    elif 'new_event' in request.GET:
        return redirect('/events/new_event')

    if request.method == 'POST':
        form_day = DateSelectionForm(request.POST)
        if form_day.is_valid():
            selected_date = form_day.cleaned_data['selected_date']
            selected_year = selected_date.year if selected_date.year is not None else selected_year
            selected_month = selected_date.month if selected_date.month is not None else selected_month
            selected_day = selected_date.day if selected_date.day is not None else selected_day

            day_of_week = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
        if 'my_button' in request.POST:
            return redirect('home')
        elif 'delete_event_id' in request.POST:  # Проверяем, было ли отправлено сообщение об удалении
            event_id = request.POST.get('delete_event_id')
            event = Event.objects.get(id=event_id)
            event.delete()  # Удаляем событие
            return redirect('day')  # Перенаправляем обратно на страницу событий после удаления
        elif 'day_select' in request.POST:
            return redirect('day_selected_day', selected_year, selected_month, selected_day)
    else:
        form_day = DateSelectionForm()
        if 'view_button' in request.GET:  # Если нажата кнопка submit при выборе отображения
            temp = request.GET.get('view type', None)  # Получаем, что выбрали
            if temp == 'month':
                return redirect('events')  # Остаемся в той же вкладке
            elif temp == 'week':
                return redirect('week')  # Летим в week, чтобы уже работать в функции week на новой странице
            elif temp == 'day':
                return redirect('day')  # Летим в day, чтобы уже работать в функции day на новой странице

        form = EventForm()

    # for element in YEARS:
    #     if element[0] == str(selected_year):
    #         name = element

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

    events = Event.objects.filter(date_start__year=selected_year,
                                  date_start__month=selected_month,
                                  user=request.user)
    month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
             'Сентябрь', 'Август', 'Ноябрь', 'Декабрь']
    hours_str = [f"{hour:02d}:00" for hour in range(1, 24)]
    hours_str.append('00:00')
    hours = []
    for i in hours_str:
        hours.append(datetime.strptime(i, '%H:%M'))

    notification = Notification.objects.filter(user=request.user)
    # YEARS[YEARS.index(name)][1]
    calendar_data = {
        'form': form, 'form_day': form_day, 'events': events,
        'current_month': month[selected_month - 1],
        'month': selected_month,
        'current_year': selected_year, 'days_of_month': days_of_month,
        'current_day': selected_day,
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
            event.description = request.POST.get('description', '')
            event.save()
            return redirect('/events')
    else:
        form = EventForm()
    return render(request, 'events/new_event.html', {'form': form})