from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
        Конфигурация приложения для главной страницы.

        Attributes
        ----------
        default_auto_field : str
            Тип поля для автоматического увеличения идентификатора.
        name : str
            Имя приложения.
        """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
