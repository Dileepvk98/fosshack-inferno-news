# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-07 16:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_articles_publishedat'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='category',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]
