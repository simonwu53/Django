# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-24 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20170424_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consult',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
