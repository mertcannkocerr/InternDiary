# Generated by Django 2.0 on 2019-08-21 12:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Working_Day_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, default='')),
                ('date', models.DateField(default=datetime.datetime(2019, 8, 21, 12, 41, 36, 443656))),
                ('related_intern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.InternUser')),
            ],
        ),
    ]
