# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('fetch/<source>', views.populate_db),
    path('sources', views.src),
]