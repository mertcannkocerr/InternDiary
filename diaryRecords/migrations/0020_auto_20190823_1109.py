# Generated by Django 2.0 on 2019-08-23 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryRecords', '0019_auto_20190823_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingdayrecord',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 8, 23, 11, 9, 3, 701918)),
        ),
    ]