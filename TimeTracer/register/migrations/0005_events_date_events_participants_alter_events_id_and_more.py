# Generated by Django 4.2.11 on 2024-04-18 12:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_alter_users_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 18, 12, 23, 8, 543806, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='events',
            name='participants',
            field=models.ManyToManyField(to='register.users'),
        ),
        migrations.AlterField(
            model_name='events',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]