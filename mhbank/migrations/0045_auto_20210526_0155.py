# Generated by Django 3.2.3 on 2021-05-25 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mhbank', '0044_auto_20210526_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='access',
            field=models.CharField(default='public', max_length=30),
        ),
        migrations.AddField(
            model_name='event',
            name='mentors',
            field=models.ManyToManyField(blank=True, to='mhbank.Account'),
        ),
    ]