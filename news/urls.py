# news/urls.py
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$',views.news_render),
    path('mark/<int:newsid>',views.mark_news),
    path('test/',views.test_func),
    url(r'^profile',views.show_profile_pg),
    url(r'^(?P<news_type>[a-z]+)$',views.news_render,name = 'news_gen'),
    # url(r'^$',views.test_func),
    path('select/<sourceid>',views.mark_sources)
]
