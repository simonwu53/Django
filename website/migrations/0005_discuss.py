# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20170420_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8)),
                ('send_id', models.CharField(max_length=10)),
                ('time', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
            ],
        ),
    ]
