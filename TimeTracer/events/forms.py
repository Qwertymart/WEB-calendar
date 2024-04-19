from django import forms
from django.forms.widgets import DateInput
from .models import events

class EventForm(forms.ModelForm):
    class Meta:
        model = events
        fields = ['name', 'date_start', 'date_finish', 'description', 'participants']
        widgets = {
            'date_start': DateInput(attrs={'class': 'datepicker'}),
            'date_finish': DateInput(attrs={'class': 'datepicker'}),
        }
