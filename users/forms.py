from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    '''
        Форма для авторизации пользователя.

        Attributes
        ----------
        username : CharField
            Поле для ввода логина.
        password : CharField
            Поле для ввода пароля.
        '''

    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        '''
        Meta : class
            Метаданные для формы.
        '''
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    '''
        Форма для регистрации нового пользователя.

        Attributes
        ----------
        username : CharField
            Поле для ввода логина.
        password1 : CharField
            Поле для ввода пароля.
        password2 : CharField
            Поле для ввода подтверждения пароля.
        labels : dict
            Метки для полей формы.
        widgets : dict
            Виджеты для полей формы.
        '''
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        '''
        Meta : class
        Метаданные для формы.
        '''
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    labels = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
    }

    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-input'}),
        'last_name': forms.TextInput(attrs={'class': 'form-input'}),
    }

    def clean_username(self):
        '''
        Проверяет, что введённый логин уникален.

        Returns
        -------
        str
            Очищенное значение логина.

        Raises
        ------
        ValidationError
            Если логин уже существует.
        '''
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже существует!')
        return username
