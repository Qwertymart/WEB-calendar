# Generated by Django 4.2.11 on 2024-04-22 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date_finish',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Окончание события'),
        ),
    ]
