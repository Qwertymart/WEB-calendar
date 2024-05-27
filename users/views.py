from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    """
        Представление для входа пользователя.

        Attributes
        ----------
        form_class : LoginUserForm
            Форма для входа пользователя.
        template_name : str
            Путь к шаблону страницы входа.
        extra_context : dict
            Дополнительный контекст для передачи в шаблон.
        """
    form_class = LoginUserForm
    template_name = 'users/login1.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    """
       Представление для регистрации нового пользователя.

       Attributes
       ----------
       form_class : RegisterUserForm
           Форма для регистрации пользователя.
       template_name : str
           Путь к шаблону страницы регистрации.
       extra_context : dict
           Дополнительный контекст для передачи в шаблон.
       success_url : str
           URL для перенаправления после успешной регистрации.
       """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


def logout_user(request):
    """
       Выйти из системы.

       Parameters
       ----------
       request : HttpRequest
           Запрос от клиента.
       """
    logout(request)
