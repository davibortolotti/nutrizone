# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 16:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ndbno', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('eqv', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.FloatField()),
                ('unit', models.CharField(max_length=10)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='nutrizone.Food')),
            ],
        ),
        migrations.AddField(
            model_name='measure',
            name='nutrient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutrient', to='nutrizone.Nutrient'),
        ),
    ]
