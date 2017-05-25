# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-20 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_course_is_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='is_teacher',
            field=models.CharField(choices=[('0', '学生'), ('1', '教师')], max_length=1, null=True),
        ),
    ]
