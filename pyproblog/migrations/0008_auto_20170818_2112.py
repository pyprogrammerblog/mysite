# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-18 21:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyproblog', '0007_auto_20170818_2056'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmailRecord',
            new_name='Email',
        ),
    ]
