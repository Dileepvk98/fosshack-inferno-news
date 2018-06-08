from django.db import models
# Create your models here.


class Post(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Articles(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    urlToImage = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=50, null=True)
    publishedAt = models.DateTimeField()
    source_id = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "info_news"

    def __str__(self):
        return self.title[:50]
