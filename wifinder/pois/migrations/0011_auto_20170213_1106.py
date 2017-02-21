# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 07:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pois', '0010_displayrole_statuses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poi',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='poi',
            name='type',
            field=models.CharField(blank=True, choices=[('indoor', 'Indoor'), ('outdoor', 'Outdoor')], max_length=800, null=True),
        ),
    ]
