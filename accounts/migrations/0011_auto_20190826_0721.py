# Generated by Django 2.0 on 2019-08-26 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190822_1256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='internuser',
            old_name='workedDayCount',
            new_name='worked_day_count',
        ),
    ]
