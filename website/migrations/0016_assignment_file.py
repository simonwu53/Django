# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 07:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0015_assignment_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment_file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='media/assignments')),
                ('time', models.DateTimeField(auto_now=True)),
                ('comments', models.TextField()),
                ('assignments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]