# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-15 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_assignment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='major',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
