# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-21 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_auto_20170515_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='first',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
