# Generated by Django 2.0 on 2019-08-22 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_employeeuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='internuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
