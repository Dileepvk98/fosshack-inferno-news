from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Articles
import json, requests
from datetime import datetime

# Create your views here.

def news_generate(request,news_type = "local"):

    # to delete old news from db
    # all_news = Articles.objects.all().delete()
    if(news_type == "sports"):
        source = "espn"
    elif(news_type == "science"):
        source = "techcrunch"
    elif(news_type == "business"):
        source = "business-insider"
    else:
        source = "the-hindu"
    
    response = requests.get("https://newsapi.org/v1/articles?source="+source+"&apiKey=74da5482c5fa4de690959100081eb0db")
    json_data = json.loads(response.text)
    
    for article in json_data["articles"]:
        result = Articles.objects.filter(title=article["title"])
        if len(result) < 1:
            if article["publishedAt"] is None:
                time = datetime.now()
            else:
                time = datetime.strptime(article["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
            news = Articles(title=article["title"],category=news_type ,short_description=article["description"], 
					url=article["url"],urlToImage=article["urlToImage"], author=article["author"],
					publishedAt=time, source_id=source)
            news.save()

    all_news = Articles.objects.filter(category=news_type)
    template = loader.get_template('index.html')
    context = {
        'all_news': all_news
    }
    return HttpResponse(template.render(context, request))
    
def test_func(requests):
    text = "<h1>Test page</h1>"
    return HttpResponse(text)
