# Generated by Django 2.0 on 2019-08-26 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20190826_0732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
        migrations.AddField(
            model_name='employeeuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/images/'),
        ),
        migrations.AddField(
            model_name='internuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/images/'),
        ),
    ]