from django.contrib import admin
from .models import users
from events.models import events

admin.site.register(users)
admin.site.register(events)