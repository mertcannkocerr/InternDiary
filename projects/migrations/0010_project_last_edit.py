# Generated by Django 2.0 on 2019-08-27 12:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20190827_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='last_edit',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 27, 12, 53, 47, 144456, tzinfo=utc)),
        ),
    ]
