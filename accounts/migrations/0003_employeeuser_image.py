# Generated by Django 2.0 on 2019-08-22 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_internuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
