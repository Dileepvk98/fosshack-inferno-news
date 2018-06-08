'''# from django.shortcuts import render
#from django.views.generic import ListView
#from django.http import HttpResponse
from datetime import datetime
from .models import Articles
import pymysql,json,requests
# Create your views here.


def populate_db():
    response = requests.get("https://newsapi.org/v1/articles?source=the-hindu&apiKey=74da5482c5fa4de690959100081eb0db")
    json_data = json.loads(response.text)
    
    for article in json_data["articles"]:
        if article["publishedAt"] is None:
            time = datetime.now()
        else:
            time = datetime.strptime(article["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
        p = Articles(title=article["title"], short_description=article["description"], url=article["url"],
                     urlToImage=article["urlToImage"], author=article["author"],
                     publishedAt=time)
        p.save()'''
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='74da5482c5fa4de690959100081eb0db')
all_articles = newsapi.get_everything(sources='the-hindu',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='the-hindu',
                                          category='business',
                                          language='en',
                                          country=i')
print(top_headlines)

