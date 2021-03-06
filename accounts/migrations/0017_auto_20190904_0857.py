# Generated by Django 2.0 on 2019-09-04 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20190904_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='internuser',
            name='begin_of_internship',
            field=models.DateField(default=datetime.date(2019, 9, 4)),
        ),
        migrations.AddField(
            model_name='internuser',
            name='end_of_internship',
            field=models.DateField(default=datetime.date(2019, 9, 4)),
        ),
        migrations.AlterField(
            model_name='internuser',
            name='worked_day_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
