# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('rank', models.PositiveIntegerField()),
                ('rating', models.FloatField()),
                ('kill', models.PositiveIntegerField()),
                ('mode', models.CharField(max_length=5)),
                ('damage', models.FloatField()),
            ],
        ),
    ]
