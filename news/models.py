# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Categories(models.Model):
    category = models.CharField(max_length=30,primary_key=True)

class Category_Source(models.Model):
    category = models.ForeignKey('Categories',to_field='category',on_delete=models.CASCADE)
    source_id = models.CharField(max_length=50)

class Articles(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    urlToImage = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=50, null=True)
    publishedAt = models.DateTimeField(null = True)
    # category = models.CharField(max_length=30)
    # source_id = models.CharField(max_length=100, blank=True)
    source_category = models.ForeignKey(Category_Source,on_delete=models.CASCADE)

    def __str__(self):
        return self.title[:50]

class MarkedNews(models.Model):
    username = models.ForeignKey(get_user_model(),to_field='username',on_delete=models.CASCADE)
    news_id = models.ForeignKey(Articles,to_field='news_id',on_delete=models.CASCADE)
