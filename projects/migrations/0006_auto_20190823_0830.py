# Generated by Django 2.0 on 2019-08-23 08:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20190822_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assign_date',
            field=models.DateField(default=datetime.date(2019, 8, 23)),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(default=datetime.date(2019, 8, 23)),
        ),
    ]
