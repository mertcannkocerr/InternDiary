# Generated by Django 2.0 on 2019-09-04 08:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_remove_project_last_edit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assign_date',
            field=models.DateField(default=datetime.date(2019, 9, 4)),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(default=datetime.date(2019, 9, 4)),
        ),
    ]