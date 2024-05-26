from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    name = models.CharField(max_length=50, verbose_name='Имя')
    date_start = models.DateField(verbose_name='Дата начала события')
    time_start = models.TimeField(verbose_name='Время начала события', blank=True)
    date_finish = models.DateField(verbose_name='Дата окончания события', blank=True, null=True)
    time_finish = models.TimeField(verbose_name='Время окончания события', blank=True)
    description = models.TextField(max_length=200, verbose_name='Описание', blank=True)
    color = models.CharField(max_length=10, verbose_name='Цвет')

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.time_start:
            self.time_start = '00:00:00'
        if self.date_start and not self.date_finish:
            self.date_finish = self.date_start
        if self.time_start and not self.time_finish:
            self.time_finish = self.time_start
        super().save(*args, **kwargs)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='notifications', blank=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        ordering = ['-created_at']

