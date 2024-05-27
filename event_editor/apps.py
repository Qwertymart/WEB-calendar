from django.apps import AppConfig


class EventEditorConfig(AppConfig):
    """
        Конфигурация приложения редактора событий.

        Attributes
        ----------
        default_auto_field : str
            Тип поля для автоматического увеличения идентификатора.
        name : str
            Имя приложения.
        """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event_editor'
