from django.urls import path
from django.conf.urls import url,include

from . import views


urlpatterns = [
    # path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'^signup/$', views.signup, name='signup'),
]