# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-11 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotest', '0005_auto_20180303_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=35)),
                ('simitag', models.CharField(max_length=35)),
                ('quality', models.CharField(max_length=70)),
                ('example_id', models.CharField(max_length=9)),
                ('example', models.CharField(max_length=270)),
            ],
        ),
        migrations.CreateModel(
            name='tagpair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=35)),
                ('simitag', models.CharField(max_length=35)),
            ],
        ),
        migrations.RenameField(
            model_name='tagpaircompare',
            old_name='simiTag',
            new_name='simitag',
        ),
    ]
