# Generated by Django 3.0.5 on 2020-05-20 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mhbank', '0028_question_change_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='verification_comment',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]