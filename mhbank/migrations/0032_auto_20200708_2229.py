# Generated by Django 3.0.4 on 2020-07-08 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mhbank', '0031_auto_20200708_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardness',
            name='question',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hardness', to='mhbank.Question'),
        ),
    ]
