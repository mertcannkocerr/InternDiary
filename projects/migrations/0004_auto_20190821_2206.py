# Generated by Django 2.0 on 2019-08-21 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20190821_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='asignee_employee',
            new_name='assignee_employee',
        ),
    ]