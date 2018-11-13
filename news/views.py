from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Articles,MarkedNews
from .models import Category_Source
from django.contrib.auth.models import User
import json, requests
from datetime import datetime
from .models import Categories
from .models import  MarkedNews

# Create your views here.

def news_fetch(news_type = "local"):

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
    try:
        for source in sources:
            response = requests.get("https://newsapi.org/v2/top-headlines?sources="+source+"&apiKey="+APIKEY)
            json_data = json.loads(response.text)
            data[source] = json_data["articles"]
    except:
        return

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
                    # eg. "2018-11-10T14:12:15Z"
                    time = datetime.strptime(time[:19]+"Z", '%Y-%m-%dT%H:%M:%SZ') 
                news = Articles(title=article["title"],short_description=article["description"], 
        				url=article["url"],urlToImage=article["urlToImage"], author=article["author"],
        				publishedAt=time,source_category=c_s_id)
                news.save()

def news_render(request,news_type = "local"):
    # news_fetch(news_type)
    all_news = Articles.objects.filter(source_category__category=news_type)
    # print(all_news)
    template = loader.get_template('index.html')
    context = {
        'all_news': all_news
    }   
    return HttpResponse(template.render(context, request))

def show_profile_pg(request):

    local = Category_Source.objects.filter(category="local")
    sports = Category_Source.objects.filter(category="sports")
    science = Category_Source.objects.filter(category="science")
    tech = Category_Source.objects.filter(category="tech")
    business = Category_Source.objects.filter(category="business")

    categories = Categories.objects.all()
    marked_news = MarkedNews.objects.all()

    context = {
        'local':local,
        'sports':sports,
        'science':science,
        'tech':tech,
        'business':business,
        
        'marked_news':marked_news,
        'categories':categories
    }

    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context, request))
    
def test_func(request):
    template = loader.get_template('test.html')
    context = {}
    return HttpResponse(template.render(context,request))

def mark_news(request,newsid,userid):
    text = "<h1>Marked/h1>"
    print(newsid,userid)
    newsOb = Articles.objects.get(news_id=newsid)
    userOb = User.objects.get(id=userid)
    m = MarkedNews(userId=userOb,news_id=newsOb)
    m.save()
    return HttpResponse(text)
