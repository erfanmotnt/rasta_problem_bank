# Generated by Django 3.0.5 on 2020-05-20 14:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mhbank', '0027_auto_20200520_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='change_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 20, 14, 10, 38, 14019, tzinfo=utc), verbose_name='date changed'),
        ),
    ]
