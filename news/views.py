from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Articles
from .models import Category_Source
import json, requests
from datetime import datetime

# Create your views here.

def news_generate(request,news_type = "local"):

    # to delete old news from db
    # all_news = Articles.objects.all().delete()
    APIKEY = "5f51f7dd9bca4908a91dd918634eb417"
    data = {}
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
        response = requests.get("https://newsapi.org/v2/top-headlines?sources="+source+"&apiKey="+APIKEY)
        json_data = json.loads(response.text)
        data[source] = json_data["articles"]

    for source in data:
        # list of articles from each source
        for article in data[source]:
            # article in list of artciles
            c_s_id = Category_Source.objects.get(category=news_type,source_id=source)
            result = Articles.objects.filter(title=article["title"])
            if len(result) < 1:
                if article["publishedAt"] is None:
                    time = datetime.now()
                else:
                    time = article["publishedAt"]
                    # time = time[:time.find('+')]+"Z"
                    time = time[:19]+"Z"
                    print("\ntime",time)
                    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ') #"2018-11-10T14:12:15Z"
                    print("\ntime",time)
                news = Articles(title=article["title"],short_description=article["description"], 
        				url=article["url"],urlToImage=article["urlToImage"], author=article["author"],
        				publishedAt=time,source_category=c_s_id)

                news.save()

    all_news = Articles.objects.filter(source_category__category=news_type)
    template = loader.get_template('index.html')
    context = {
        'all_news': all_news
    }
    return HttpResponse(template.render(context, request))
    
def test_func(requests):
    text = "<h1>Test page</h1>"
    return HttpResponse(text)
