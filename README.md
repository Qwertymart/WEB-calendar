# WEB-calendar TimeTracer

## Описание

Timetracer - это веб-приложение, разработанное для управления событиями и встречами. С его помощью пользователи могут легко добавлять, редактировать и удалять события, а также просматривать их в удобном интерфейсе.

## Функциональные возможности

- Регистрация с хешированием пароля и авторизация пользователей.
- Создание событий с указанием времени, даты и периодичности, а также их редактирование и удаление.
- Возможность добавления описания для события самостоятельно или с помощью нейросети от СБЕР GigaChat.
- Изменение времени и даты события с помощью перетаскивания.
- Напоминания о предстоящих событиях.
- Изменение цвета события для лучшей кастомизации.
- Просмотр календаря в различных режимах (день, неделя, месяц).
- Хранение захешированных данных о событиях и пользователях в базе данных SQLite.

## Необходимое ПО

- Python 3.12+
- Django 4.0.4+
- langchain 0.1.19+
- gigachain 0.1.17+
- gigachain-cli 0.0.21+
- gigachat 0.1.23+

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Qwertymart/WEB-calendar.git
    cd WEB-calendar
    ```
2. Создайте виртуальное окружение и активируйте его, если нужно:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```
3. Установите необходимое ПО:
    ```bash
    pip install -r requirements.txt
    ```
4. Выполните миграции базы данных:
    ```bash
    python manage.py migrate
    ```
5. Создайте суперпользователя для доступа к админ-панели:
    ```bash
    python manage.py createsuperuser
    ```

## Запуск

Запуск сервера:
```bash
python manage.py runserver
```

##Подробнее о нашей работе

Доска Miro с таймлайном, таск-трекером:
https://miro.com/app/board/uXjVNqIUDdM=/
