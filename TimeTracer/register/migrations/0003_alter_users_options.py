# Generated by Django 4.2.11 on 2024-03-31 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_events'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name_plural': 'Users'},
        ),
    ]