# Generated by Django 2.0 on 2019-08-22 12:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryRecords', '0015_auto_20190822_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='working_day_record',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 8, 22, 12, 52, 3, 73769)),
        ),
    ]
