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


TYPES = (
    ('month', 'month'),
    ('week', 'week'),
    ('day', 'day')
)
WEEKS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
)


class ViewTypeForm(forms.Form):
    type = forms.ChoiceField(choices=TYPES)


class WeekNumberForm(forms.Form):
    number_of_week = forms.ChoiceField(choices=WEEKS)
