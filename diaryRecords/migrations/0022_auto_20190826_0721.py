# Generated by Django 2.0 on 2019-08-26 07:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryRecords', '0021_auto_20190823_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingdayrecord',
            name='date',
            field=models.DateField(default=datetime.date(2019, 8, 26)),
        ),
    ]
