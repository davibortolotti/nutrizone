# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrizone', '0004_auto_20170803_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='specialmeasure',
            new_name='altmeasurename',
        ),
        migrations.AddField(
            model_name='food',
            name='altmeasuregram',
            field=models.FloatField(default=0),
        ),
    ]
