# Generated by Django 2.0 on 2019-09-09 14:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20190904_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internuser',
            name='begin_of_internship',
            field=models.DateField(default=datetime.date(2019, 9, 9)),
        ),
        migrations.AlterField(
            model_name='internuser',
            name='end_of_internship',
            field=models.DateField(default=datetime.date(2019, 9, 9)),
        ),
    ]
