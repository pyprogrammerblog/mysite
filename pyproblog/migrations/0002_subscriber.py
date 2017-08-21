# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-12 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pyproblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateField(auto_now_add=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('email_verification_code', models.UUIDField(default=uuid.uuid4, null=True)),
            ],
        ),
    ]
