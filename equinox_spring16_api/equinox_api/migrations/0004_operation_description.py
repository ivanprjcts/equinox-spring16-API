# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equinox_api', '0003_instances'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='description',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
