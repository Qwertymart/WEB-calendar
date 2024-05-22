# Generated by Django 4.0.4 on 2024-05-21 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, max_length=200, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_finish',
            field=models.TimeField(blank=True, verbose_name='Время окончания события'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_start',
            field=models.TimeField(blank=True, verbose_name='Время начала события'),
        ),
    ]