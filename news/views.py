# from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from datetime import datetime
from .models import Articles
import json, requests
# Create your views here.


def populate_db(request, source):
    response = requests.get("https://newsapi.org/v1/articles?source="+source+"&apiKey=74da5482c5fa4de690959100081eb0db")
    json_data = json.loads(response.text)
    for article in json_data["articles"]:
        result = Articles.objects.filter(title=article["title"])
        if len(result) != 1:
            if article["publishedAt"] is None:
                time = datetime.now()
            else:
                time = datetime.strptime(article["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
            p = Articles(title=article["title"], short_description=article["description"], url=article["url"],
                         urlToImage=article["urlToImage"], author=article["author"],
                         publishedAt=time, source_id=source)
            p.save()
    return HttpResponse("Fetched News from "+source)


def src(request):
    response = requests.get("https://newsapi.org/v1/sources?language=en")
    json_data = json.loads(response.text)
    string = ""
    for i in json_data["sources"]:
        string = string+"<br>"+i["id"]

    return HttpResponse("Sources List " + string)


class HomePageView(ListView):
    model = Articles
    template_name = 'home.html'
