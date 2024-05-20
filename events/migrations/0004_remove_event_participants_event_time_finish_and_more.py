# Generated by Django 4.2.11 on 2024-05-09 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_participant_event_participants_delete_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
        migrations.AddField(
            model_name='event',
            name='time_finish',
            field=models.TimeField(default='00:00:00', verbose_name='Время окончания события'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='time_start',
            field=models.TimeField(default='00:00:00', verbose_name='Время начала события'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='date_finish',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания события'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateField(verbose_name='Дата начала события'),
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
    ]