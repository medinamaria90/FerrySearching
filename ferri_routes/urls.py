
from django.urls import include, path
from . import views

from django.shortcuts import render 
# import json to load json data to python dictionary 
import json 
# urllib.request to make a request to api 
import urllib.request 

urlpatterns = [
    path('', views.index, name="index"),
]
