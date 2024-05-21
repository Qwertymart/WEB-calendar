from django import forms
from django.forms.widgets import DateInput
from .models import Event


class EventForm(forms.ModelForm):
    PERIODICITY_CHOICES = [
        ('no repeat', 'Не повторять'),
        ('daily', 'Дневная'),
        ('weekly', 'Недельная'),
        ('monthly', 'Месячная'),
        ('yearly', 'Годовая'),
    ]

    periodicity = forms.ChoiceField(
        choices=PERIODICITY_CHOICES,
        required=True,
        label='Периодичность'
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        label='Конечная дата'
    )

    class Meta:
        model = Event
        fields = ['name', 'date_start', 'time_start', 'date_finish', 'time_finish', 'description', 'color',
                  'periodicity', 'end_date']
        widgets = {
            'date_start': forms.DateInput(attrs={'class': 'datepicker'}),
            'time_start': forms.TimeInput(attrs={'class': 'timepicker'}),
            'date_finish': forms.DateInput(attrs={'class': 'datepicker'}),
            'time_finish': forms.TimeInput(attrs={'class': 'timepicker'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        periodicity = cleaned_data.get('periodicity')
        end_date = cleaned_data.get('end_date')

        if periodicity != 'no repeat' and not end_date:
            self.add_error('end_date', 'Это поле обязательно для выбранной периодичности.')

        return cleaned_data

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
    ('5', '5'),
)
MONTHS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12')
)
YEARS = (
    ('1', '2015'),
    ('2', '2016'),
    ('3', '2017'),
    ('4', '2018'),
    ('5', '2019'),
    ('6', '2020'),
    ('7', '2021'),
    ('8', '2022'),
    ('9', '2023'),
    ('10', '2024'),
    ('11', '2025'),
    ('12', '2026'),
    ('13', '2027'),
    ('14', '2028'),
    ('15', '2029'),
    ('16', '2030')
)


class ViewTypeForm(forms.Form):
    type = forms.ChoiceField(choices=TYPES)


class DateSelectionForm(forms.Form):
    selected_date = forms.DateField(label='', widget=forms.SelectDateWidget())


class WeekNumberForm(forms.Form):
    number_of_week = forms.ChoiceField(choices=WEEKS)


class MonthSelect(forms.Form):
    selected_month = forms.ChoiceField(choices=MONTHS)


class YearSelect(forms.Form):
    selected_year = forms.ChoiceField(choices=YEARS)


class DayView(forms.Form):
    day_select_form = forms.DateTimeField()
    widget = forms.DateInput(
        attrs={
            'class': 'form_control',
            'type': 'date'
        }
    )
