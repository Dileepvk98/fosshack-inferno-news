# from django.shortcuts import render
from django.views.generic import ListView
from .models import Articles

# Create your views here.


class HomePageView(ListView):
    model = Articles
    template_name = 'home.html'
