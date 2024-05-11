from django.contrib import admin
from events.models import Event, Notification

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_start', 'time_start', 'date_finish', 'time_finish', 'description')

admin.site.register(Event, EventAdmin)
admin.site.register(Notification)

