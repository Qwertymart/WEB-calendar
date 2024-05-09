from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    name = models.CharField(max_length=50, verbose_name='Имя')
    date_start = models.DateField(verbose_name='Дата начала события')
    time_start = models.TimeField(verbose_name='Время начала события')
    date_finish = models.DateField(verbose_name='Дата окончания события', blank=True, null=True)
    time_finish = models.TimeField(verbose_name='Время окончания события')
    description = models.CharField(max_length=200, verbose_name='Описание')

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.date_start and not self.date_finish:
            self.date_finish = self.date_start
        if self.time_start and not self.time_finish:
            self.time_finish = self.time_start
        super().save(*args, **kwargs)
