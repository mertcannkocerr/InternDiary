# Generated by Django 2.0 on 2019-08-27 12:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20190826_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assign_date',
            field=models.DateField(default=datetime.date(2019, 8, 27)),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(default=datetime.date(2019, 8, 27)),
        ),
    ]