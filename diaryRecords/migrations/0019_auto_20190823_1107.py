# Generated by Django 2.0 on 2019-08-23 11:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryRecords', '0018_auto_20190823_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingdayrecord',
            name='enable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='workingdayrecord',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 8, 23, 11, 7, 51, 503296)),
        ),
    ]
