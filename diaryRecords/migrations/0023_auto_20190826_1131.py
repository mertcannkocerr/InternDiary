# Generated by Django 2.0 on 2019-08-26 11:31

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diaryRecords', '0022_auto_20190826_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingdayrecord',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
    ]