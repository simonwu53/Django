# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_assignment_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment_file',
            name='comments',
            field=models.TextField(null=True),
        ),
    ]
