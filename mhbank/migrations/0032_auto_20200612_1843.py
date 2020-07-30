# Generated by Django 3.0.4 on 2020-06-12 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mhbank', '0031_auto_20200612_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='guidance',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='teach_box',
            name='expectations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teach_box',
            name='generalـprocess',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='teach_box',
            name='goal',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='themed_q',
            name='text',
            field=models.TextField(),
        ),
    ]
