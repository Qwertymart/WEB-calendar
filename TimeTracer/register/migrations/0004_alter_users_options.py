# Generated by Django 4.2.11 on 2024-04-01 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_users_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
