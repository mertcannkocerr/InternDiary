# Generated by Django 2.0 on 2019-09-12 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20190912_0006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='address',
            new_name='company_address',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='name',
            new_name='company_name',
        ),
    ]
