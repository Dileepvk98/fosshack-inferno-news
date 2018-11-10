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
    sources=[]
    data = []
    if(news_type == "sports"):
        sources = ["espn","bbc-sport","espn-cric-info","football-italia"]
        
    elif(news_type == "science"):
        sources = ["new-scientist","next-big-future","national-geographic"]

    elif(news_type == "tech"):
        sources = ["techcrunch","ars-technica","wired","ign"]

    elif(news_type == "business"):
        sources = ["business-insider","cnbc","financial-times"]
        
    else:
        sources = ["the-hindu","the-times-of-india","google-news-in"]
    
    for source in sources:
        response = requests.get("https://newsapi.org/v2/top-headlines?sources="+source+"&apiKey=d76f9ebaf17c4088ba4db2a030194f4c")
        json_data = json.loads(response.text)
        data.append(json_data["articles"])

    for articles in data:
        # list of articles from each source
        for article in articles:
            # article in list of artciles
            result = Articles.objects.filter(title=article["title"])
            if len(result) < 1:
                # if article["publishedAt"] is None:
                #     time = datetime.now()
                # else:
                #     time = datetime.strptime(article["publishedAt"], '%Y-%m-%dT%H:%M:%SZ') "2018-11-10T14:12:15Z"
                news = Articles(title=article["title"],category=news_type ,short_description=article["description"], 
        				url=article["url"],urlToImage=article["urlToImage"], author=article["author"],
        				# publishedAt=time,
                         source_id=article["source"]["name"])
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
