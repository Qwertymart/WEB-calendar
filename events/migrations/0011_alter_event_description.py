# Generated by Django 4.0.4 on 2024-05-27 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_merge_20240526_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, max_length=5000, verbose_name='Описание'),
        ),
    ]
