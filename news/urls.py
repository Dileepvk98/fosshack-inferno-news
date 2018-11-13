# news/urls.py
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^(?P<news_type>[a-z]+)$',views.news_render,name = 'news_render'),
    # url(r'^$',views.test_func),
    url(r'^$',views.news_render),
    path('mark/<int:newsid>/<int:userid>',views.mark_news),
    path('test/',views.test_func)
]
