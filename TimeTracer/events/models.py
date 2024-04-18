from django.db import models
from register.models import users

class events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Имя')
    date_start = models.DateTimeField(verbose_name='Начало события')
    date_finish = models.DateTimeField(verbose_name='Окончание события')
    description = models.CharField(max_length=200, verbose_name='Описание')
    participants = models.ManyToManyField(users, verbose_name='Соучастники')

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name
