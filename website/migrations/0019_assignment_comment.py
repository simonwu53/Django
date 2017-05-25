# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-15 09:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0018_remove_assignment_file_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment_comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10, null=True)),
                ('last_name', models.CharField(max_length=10, null=True)),
                ('comment', models.TextField()),
                ('assignment_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Assignment_file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
