# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-01 12:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_auto_20190228_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
