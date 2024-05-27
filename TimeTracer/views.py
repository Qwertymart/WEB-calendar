from django.shortcuts import render

import datetime


def home(request):
    '''
        Обрабатывает запрос к главной странице.

        Parameters
        ----------
        request : HttpRequest
            Запрос от клиента.

        Returns
        -------
        HttpResponse
            Ответ с отрендеренной главной страницей.
        '''
    date = datetime.datetime.now().date()
    return render(request, 'home.html')
