# Generated by Django 3.2.5 on 2021-08-10 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20210809_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='date_of_dead',
            new_name='date_of_death',
        ),
    ]