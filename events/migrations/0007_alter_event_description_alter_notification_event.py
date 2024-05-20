# Generated by Django 4.0.4 on 2024-05-11 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_notification_event_alter_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=200, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='event',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='events.event'),
        ),
    ]