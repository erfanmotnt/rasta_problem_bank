# Generated by Django 3.0.5 on 2020-05-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mhbank', '0030_remove_question_change_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='change_date',
            field=models.DateTimeField(null=True, verbose_name='date changed'),
        ),
    ]