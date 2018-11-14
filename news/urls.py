# news/urls.py
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$',views.news_render),
    url(r'^profile',views.show_profile_pg),
    path('mark/<int:newsid>/<int:userid>',views.mark_news),
    path('test/',views.test_func),
    url(r'^(?P<news_type>[a-z]+)$',views.news_render,name = 'news_gen')
    # url(r'^$',views.test_func),
]
