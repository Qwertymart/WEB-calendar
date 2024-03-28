from django.contrib import admin
from .models import users, events

admin.site.register(users)
admin.site.register(events)