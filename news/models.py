# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Articles(models.Model):
    news_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=30)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=200)
    urlToImage = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=50, null=True)
    publishedAt = models.DateTimeField(null = True)
    source_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title[:50]
