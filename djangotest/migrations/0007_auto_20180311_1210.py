# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-11 04:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotest', '0006_auto_20180311_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='example',
            field=models.CharField(max_length=300),
        ),
    ]
