from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
import json, requests
from datetime import datetime
from .models import Articles,MarkedNews,Category_Source,SourcesSelected

# Create your views here.
def news_fetch(request,news_type):
    APIKEY = "5f51f7dd9bca4908a91dd918634eb417"
    data = {}
    if request.user.is_authenticated:
        selected_sources = SourcesSelected.objects.filter(userId=request.user.id,source_id__category=news_type)
        selected_sources = [s.source_id.source_id for s in selected_sources]
        print("Selected",selected_sources)
    else:
        selected_sources = Category_Source.objects.filter(category=news_type)
        selected_sources = [s.source_id for s in selected_sources]
        print("All",selected_sources)
    
    try:
        for source in selected_sources:
            print("Fetched news from ",source)
            response = requests.get("https://newsapi.org/v2/top-headlines?sources="+source+"&apiKey="+APIKEY)
            json_data = json.loads(response.text)
            data[source] = json_data["articles"]
    except:
        return selected_sources

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
                    time = article["publishedAt"]# eg. "2018-11-10T14:12:15Z"
                    time = datetime.strptime(time[:19]+"Z", '%Y-%m-%dT%H:%M:%SZ') 
                news = Articles(title=article["title"],short_description=article["description"], 
        				url=article["url"],urlToImage=article["urlToImage"], author=article["author"],
        				publishedAt=time,source_category=c_s_id)
                news.save()
    
    return selected_sources

def news_render(request,news_type = "local"):
    selected_sources = news_fetch(request,news_type)
    marked = []
    all_news = Articles.objects.filter(source_category__category=news_type,source_category__source_id__in=selected_sources)
    if request.user.is_authenticated:
        marked = MarkedNews.objects.filter(userId=request.user.id)
        marked = [m.news_id.news_id for m in marked]

    template = loader.get_template('index.html')
    context = {
        'all_news': all_news,
        'marked_news':marked
    }   
    return HttpResponse(template.render(context, request))

def show_profile_pg(request):
    if request.method == 'GET':
        newsid = request.GET.get('news')
        if newsid is not None:
            MarkedNews.objects.filter(news_id=newsid,userId=request.user.id).delete()
    local = Category_Source.objects.filter(category="local")
    sports = Category_Source.objects.filter(category="sports")
    science = Category_Source.objects.filter(category="science")
    tech = Category_Source.objects.filter(category="tech")
    business = Category_Source.objects.filter(category="business")
    marked_news = MarkedNews.objects.filter(userId=request.user.id)
    selected_sources = SourcesSelected.objects.filter(userId=request.user.id)
    selected_sources = [s.source_id.source_id for s in selected_sources]
    print(selected_sources)
    context = {
        'local':local,
        'sports':sports,
        'science':science,
        'tech':tech,
        'business':business,
        'marked_news':marked_news,
        'selected_sources':selected_sources
    }
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context, request))

def mark_news(request,newsid):
    text = "<h1>Marked/h1>"
    duplicate = MarkedNews.objects.filter(news_id=newsid,userId=request.user.id)
    if len(duplicate) < 1:
        newsOb = Articles.objects.get(news_id=newsid)
        userOb = User.objects.get(id=request.user.id)
        m = MarkedNews(userId=userOb,news_id=newsOb)
        m.save()
    else:
        MarkedNews.objects.filter(news_id=newsid,userId=request.user.id).delete()
    return HttpResponse(text)

def mark_sources(request,sourceid):
    text = "<h1>Source Selected/h1>"
    print(sourceid)
    duplicate = SourcesSelected.objects.filter(source_id__source_id=sourceid,userId=request.user.id)
    if len(duplicate) < 1:
        userOb = User.objects.get(id=request.user.id)
        sourceOb = Category_Source.objects.get(source_id=sourceid)
        m = SourcesSelected(source_id=sourceOb,userId=userOb)
        m.save()
    else:
        SourcesSelected.objects.filter(source_id__source_id=sourceid,userId=request.user.id).delete()
    return HttpResponse(text)
    
def test_func(request):
    template = loader.get_template('test.html')
    context = {}
    return HttpResponse(template.render(context,request))