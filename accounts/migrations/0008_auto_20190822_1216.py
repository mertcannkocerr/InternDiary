# Generated by Django 2.0 on 2019-08-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190822_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='acoounts/images/'),
        ),
        migrations.AlterField(
            model_name='internuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/images/'),
        ),
    ]