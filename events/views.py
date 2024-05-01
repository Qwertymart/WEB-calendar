# views.py
from django.shortcuts import render, redirect
from .forms import EventForm, ViewTypeForm, YEARS
from .models import Event as Event
from django.utils import timezone
from datetime import datetime
from calendar import monthrange


def events(request):
    def select_view():
        global flag_month, flag_week, flag_day

        flag_month = False
        flag_week = False
        flag_day = False
        temp = request.GET.get('view type', None)  # Получаем, что выбрали
        if temp == 'week':
            flag_week = True
            return flag_week
        elif temp == 'day':
            flag_day = True
            return flag_day
        elif temp == 'month':
            flag_month = True
            return flag_month

    if request.method == 'POST':
        if 'my_button' in request.POST:
            return redirect('home')
        elif 'delete_event_id' in request.POST:  # Проверяем, было ли отправлено сообщение об удалении
            event_id = request.POST.get('delete_event_id')
            event = Event.objects.get(id=event_id)
            event.delete()  # Удаляем событие
            return redirect('/events')  # Перенаправляем обратно на страницу событий после удаления
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.save()
                return redirect('/events')
    else:
        if 'view_button' in request.GET:  # Если нажата кнопка submit при выборе отображения
            select_view()
            if flag_month:
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
                month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
                         'Сентябрь', 'Август', 'Ноябрь', 'Декабрь']
                return render(request, 'events/events.html',
                              {'form': form, 'events': events, 'current_month': current_month,
                               'current_year': current_year,
                               'days_of_month': days_of_month, 'flag_month': flag_month,
                               'selected_month': month[selected_month - 1], 'selected_year': selected_year})
            elif flag_week:

                form = EventForm()
                current_month = timezone.now().month
                current_year = timezone.now().year
                selected_week = 1
                selected_month = request.GET.get('selected_month', None)
                selected_year = request.GET.get('selected_year', None)
                if 'week_to_show' in request.GET:

                    if selected_month is None:
                        current_month = timezone.now().month
                        selected_month = current_month
                    else:
                        current_month = int(selected_month)
                    if selected_year is None:
                        current_year = timezone.now().year
                    else:
                        current_year = int(selected_year)
                    selected_week = int(request.GET.get('number_of_week', '1'))
                for value in YEARS:
                    if value[1] == str(timezone.now().year):
                        name = value

                current_year = int(YEARS[YEARS.index(name)][1])
                first_weekday, num_days = monthrange(current_year, current_month)
                num_padding_days = (first_weekday) % 7
                days_of_month = []
                week_of_month = []
                for i in range(num_padding_days):
                    week_of_month.append(None)
                for day_of_month in range(1, num_days + 1):
                    week_of_month.append(datetime(current_year, current_month, day_of_month))
                    if len(week_of_month) == 7:
                        days_of_month.append(week_of_month)
                        week_of_month = []
                if week_of_month:
                    while len(week_of_month) < 7:
                        week_of_month.append(None)
                    days_of_month.append(week_of_month)

                current_week = days_of_month[selected_week - 1]
                week_counter = len(days_of_month)
                options = []
                for number in range(week_counter):
                    options.append({'value': f'{number + 1}', 'label': f'{number + 1}'})

                hours = [f"{hour:02d}:00" for hour in range(1, 25)]
                month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
                         'Сентябрь', 'Август', 'Ноябрь', 'Декабрь']

                return render(request, 'events/events.html',
                              {'current_month': month[current_month - 1],
                               'current_year': YEARS[YEARS.index(name)][1],
                               'days_of_month': days_of_month, 'current_week': current_week, 'options': options,
                               'flag_week': flag_week, 'hours': hours, 'selected_month': selected_month,
                               'selected_year': selected_year, 'selected_week': selected_week})

            elif flag_day:
                return redirect('day')  # Летим в day, чтобы уже работать в функции day на новой странице

        elif 'week_to_show' in request.GET:
            if flag_week:

                form = EventForm()
                current_month = timezone.now().month
                current_year = timezone.now().year
                selected_week = 1

                if 'week_to_show' in request.GET:
                    selected_month = request.GET.get('selected_month', None)
                    selected_year = request.GET.get('selected_year', None)
                    if selected_month is None:
                        current_month = timezone.now().month
                        selected_month = current_month
                    else:
                        current_month = int(selected_month)
                    if selected_year is None:
                        current_year = timezone.now().year
                    else:
                        current_year = int(selected_year)
                    selected_week = int(request.GET.get('number_of_week', '1'))
                for value in YEARS:
                    if value[1] == str(timezone.now().year):
                        name = value

                current_year = int(YEARS[YEARS.index(name)][1])
                first_weekday, num_days = monthrange(current_year, current_month)
                num_padding_days = (first_weekday) % 7
                days_of_month = []
                week_of_month = []
                for i in range(num_padding_days):
                    week_of_month.append(None)
                for day_of_month in range(1, num_days + 1):
                    week_of_month.append(datetime(current_year, current_month, day_of_month))
                    if len(week_of_month) == 7:
                        days_of_month.append(week_of_month)
                        week_of_month = []
                if week_of_month:
                    while len(week_of_month) < 7:
                        week_of_month.append(None)
                    days_of_month.append(week_of_month)

                current_week = days_of_month[selected_week - 1]
                week_counter = len(days_of_month)
                options = []
                for number in range(week_counter):
                    options.append({'value': f'{number + 1}', 'label': f'{number + 1}'})

                return render(request, 'events/events.html',
                              {'current_month': current_month,
                               'current_year': YEARS[YEARS.index(name)][1],
                               'days_of_month': days_of_month, 'current_week': current_week, 'options': options,
                               'flag_week': flag_week})

            elif flag_day:
                return redirect('day')  # Летим в day, чтобы уже работать в функции day на новой странице
        form = EventForm()

    current_year = timezone.now().year
    current_month = timezone.now().month
    current_day = timezone.now().day

    selected_month = int(request.GET.get('selected_month', current_month))
    selected_year = int(request.GET.get('selected_year', current_year))
    month = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ', 'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ']
    select_month = month[selected_month - 1]
    cur_month = month[current_month - 1]

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

    return render(request, 'events/events.html',
                  {'form': form, 'events': events, 'current_month': current_month, 'current_year': current_year,
                   'days_of_month': days_of_month, 'selected_month': selected_month, 'selected_year': selected_year,
                   'current_day': current_day, 'select_month': select_month, 'cur_month': cur_month})


# def week(request):
#     if request.method == 'POST':
#         if 'my_button' in request.POST:
#             return redirect('home')
#         elif 'delete_event_id' in request.POST:  # Проверяем, было ли отправлено сообщение об удалении
#             event_id = request.POST.get('delete_event_id')
#             event = Event.objects.get(id=event_id)
#             event.delete()  # Удаляем событие
#             return redirect('week')  # Перенаправляем обратно на страницу событий после удаления
#         else:
#             form = EventForm(request.POST)
#             if form.is_valid():
#                 event = form.save(commit=False)
#                 event.user = request.user
#                 event.save()
#                 return redirect('week')
#     else:
#         if 'view_button' in request.GET:  # Если нажата кнопка submit при выборе отображения
#             context = {}
#             form = ViewTypeForm()
#             context['form'] = form
#             temp = request.GET.get('view type', None)  # Получаем, что выбрали
#             if temp == 'month':
#                 # form = EventForm()
#                 return redirect('events')  # Остаемся в той же вкладке
#             elif temp == 'week':
#                 return redirect('week')  # Летим в week, чтобы уже работать в функции week на новой странице
#             elif temp == 'day':
#                 return redirect('day')  # Летим в day, чтобы уже работать в функции day на новой странице
#
#         form = EventForm()
#     current_month = timezone.now().month
#     current_year = timezone.now().year
#     selected_week = 1
#     if 'week_to_show' in request.GET:
#         selected_month = request.GET.get('selected_month', None)
#         selected_year = request.GET.get('selected_year', None)
#         if selected_month is None:
#             current_month = timezone.now().month
#         else:
#             current_month = int(selected_month)
#         if selected_year is None:
#             current_year = timezone.now().year
#         else:
#             current_year = int(selected_year)
#         selected_week = int(request.GET.get('number_of_week', '1'))
#     for value in YEARS:
#         if value[1] == str(timezone.now().year):
#             name = value
#
#     current_year = int(YEARS[YEARS.index(name)][1])
#     first_weekday, num_days = monthrange(current_year, current_month)
#     num_padding_days = (first_weekday) % 7
#     days_of_month = []
#     week_of_month = []
#     for i in range(num_padding_days):
#         week_of_month.append(None)
#     for day_of_month in range(1, num_days + 1):
#         week_of_month.append(datetime(current_year, current_month, day_of_month))
#         if len(week_of_month) == 7:
#             days_of_month.append(week_of_month)
#             week_of_month = []
#     if week_of_month:
#         while len(week_of_month) < 7:
#             week_of_month.append(None)
#         days_of_month.append(week_of_month)
#
#     current_week = days_of_month[selected_week - 1]
#     week_counter = len(days_of_month)
#     options = []
#     for number in range(week_counter):
#         options.append({'value': f'{number + 1}', 'label': f'{number + 1}'})
#
#     #events = Event.objects.filter(date_start__year=current_year, date_start__month=current_month, user=request.user)
#
#     return render(request, 'events/week.html',
#                   {'form': form, 'events': events, 'current_month': current_month,
#                    'current_year': YEARS[YEARS.index(name)][1],
#                    'days_of_month': days_of_month, 'current_week': current_week, 'options': options})
#

def day(request):
    if request.method == 'POST':
        if 'my_button' in request.POST:
            return redirect('home')
        elif 'delete_event_id' in request.POST:  # Проверяем, было ли отправлено сообщение об удалении
            event_id = request.POST.get('delete_event_id')
            event = Event.objects.get(id=event_id)
            event.delete()  # Удаляем событие
            return redirect('/events')  # Перенаправляем обратно на страницу событий после удаления
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.save()
                return redirect('/events')
    else:
        if 'view_button' in request.GET:  # Если нажата кнопка submit при выборе отображения
            context = {}
            form = ViewTypeForm()
            context['form'] = form
            temp = request.GET.get('view type', None)  # Получаем, что выбрали
            if temp == 'month':
                # form = EventForm()
                return redirect('events')  # Остаемся в той же вкладке
            elif temp == 'week':
                return redirect('week')  # Летим в week, чтобы уже работать в функции week на новой странице
            elif temp == 'day':
                return redirect('day')  # Летим в day, чтобы уже работать в функции day на новой странице

        form = EventForm()
    current_month = timezone.now().month
    current_year = timezone.now().year
    selected_week = 1
    if 'week_to_show' in request.GET:
        selected_month = request.GET.get('selected_month', None)
        selected_year = request.GET.get('selected_year', None)
        if selected_month is None:
            current_month = timezone.now().month
        else:
            current_month = int(selected_month)
        if selected_year is None:
            current_year = timezone.now().year
        else:
            current_year = int(selected_year)
        selected_week = int(request.GET.get('number_of_week', '1'))

    for value in YEARS:
        if value[1] == str(timezone.now().year):
            name = (value[0], str(timezone.now().year))
    # name = (str(i for i in YEARS if i[1] == str(timezone.now().year)), str(timezone.now().year))

    for element in YEARS:
        if element[0] == str(current_year):
            name = element

    current_year = int(YEARS[YEARS.index(name)][1])
    first_weekday, num_days = monthrange(current_year, current_month)
    num_padding_days = (first_weekday) % 7
    days_of_month = []
    week_of_month = []
    for i in range(num_padding_days):
        week_of_month.append(None)
    for day_of_month in range(1, num_days + 1):
        week_of_month.append(datetime(current_year, current_month, day_of_month))
        if len(week_of_month) == 7:
            days_of_month.append(week_of_month)
            week_of_month = []
    if week_of_month:
        while len(week_of_month) < 7:
            week_of_month.append(None)
        days_of_month.append(week_of_month)

    current_week = days_of_month[selected_week - 1]
    week_counter = len(days_of_month)
    options = []
    for number in range(week_counter):
        options.append({'value': f'{number + 1}', 'label': f'{number + 1}'})

    # events = Event.objects.filter(date_start__year=current_year, date_start__month=current_month, user=request.user)

    return render(request, 'events/day.html',
                  {'form': form, 'events': events, 'current_month': current_month,
                   'current_year': YEARS[YEARS.index(name)][1],
                   'days_of_month': days_of_month, 'current_week': current_week, 'options': options})

    return render(request, 'events/day.html')
